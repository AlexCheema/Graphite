import asyncio
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx
import os

load_dotenv()  # take environment variables from .env.
api_key = os.getenv('THEGRAPH_API_KEY')

async def get_pools(token0=None, token1=None):
  transport = RequestsHTTPTransport(url='https://gateway-arbitrum.network.thegraph.com/api/56c79aa4c0aee0d175eab847b146f550/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B')
  client = Client(transport=transport, fetch_schema_from_transport=True)

  # Define the GraphQL query
  # Filter by pools with token0.name and token1.name if both are provided
  token0_filter = f'token0:"{token0}"' if token0 else ''
  token1_filter = f'token1:"{token1}"' if token1 else ''
  token_filter = 'and: [{' + token0_filter + '}, {' + token1_filter + '}]' if token0_filter and token1_filter else f'{token0_filter} {token1_filter}'
  query = gql(f'''
  {{
    pools(first: 5, where:{{ {token_filter} }}) {{
      id
    	liquidity
    	tick
    	sqrtPrice
      token0 {{
        id
        name
        symbol
        decimals

      }}
      token1 {{
        id
        name
        symbol
        decimals
      }}
    }}
  }}
  ''')

  result = client.execute(query)
  print(result)
  return result

def parse_pools(data):
  # Creating an intermediate data structure for token transfers
  pools = []

  for pool in data['pools']:
      liquidity = int(pool['liquidity'])
      tick = int(pool['tick'])
      sqrt_price_x96 = int(pool['sqrtPrice'])
      token0 = {
         'name': pool['token0']['name'],
         'symbol': pool['token0']['symbol'],
         'decimals': int(pool['token0']['decimals']),
      }
      token1 = {
         'name': pool['token1']['name'],
         'symbol': pool['token1']['symbol'],
         'decimals': int(pool['token1']['decimals']),
      }

      # Convert sqrt_price_x96 from x96 fixed point to a decimal
      sqrt_price = sqrt_price_x96 / (2**96)
      price = (sqrt_price * sqrt_price) * (10**(token0['decimals'] - token1['decimals']))

      # Adding the transfer information to the list
      pools.append({
          'liquidity': liquidity,
          'tick': tick,
          'sqrt_price': sqrt_price,
          'price': price,
          'token0': token0,
          'token1': token1
      })

  return pools

def create_graph_representation(pools):
   # Creating an intermediate representation of the graph using a map
  graph_representation = {}

  for pool in pools:
      token0_symbol = pool['token0']['symbol']
      token1_symbol = pool['token1']['symbol']
      liquidity = pool['liquidity']
      tick = pool['tick']
      price = pool['price']

      # Initialize the node if not already present
      if token0_symbol not in graph_representation:
          graph_representation[token0_symbol] = {}
      if token1_symbol not in graph_representation:
          graph_representation[token1_symbol] = {}

      # Adding transfer information to the graph
      if not token1_symbol in graph_representation[token0_symbol]:
          graph_representation[token0_symbol][token1_symbol] = []

      graph_representation[token0_symbol][token1_symbol].append({
          'pool_info': {
              'liquidity': liquidity,
              'tick': tick,
              'price': price,
          },
      })

  return graph_representation

def create_approx_graph(graph_representation):
  # Creating a directed graph using the intermediate representation
  G = nx.DiGraph()

  # Iterating over the intermediate representation to create nodes and edges
  for token0_symbol, o in graph_representation.items():
      for token1_symbol, pools in o.items():
          for pool in pools:
            pool_info = pool['pool_info']
            # token_info = transfer_details['token_info']  # This can be included if needed

            # Adding nodes
            if token0_symbol not in G:
                G.add_node(token0_symbol)
            if token1_symbol not in G:
                G.add_node(token1_symbol)

            G.add_edge(token0_symbol, token1_symbol, weight=pool_info['price'])

  return G


def draw_graph(G):
  # Drawing the graph with a multi-edge layout
  pos = nx.spring_layout(G)

  # Draw the nodes
  nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)

  # Draw the edges
  for u, v, data in G.edges(data=True):
      nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=data['weight'])

  edge_labels = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

  plt.title("Token Transfer Graph")
  plt.show()


async def main():
  USDC_TOKEN_ADDR = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
  USDT_TOKEN_ADDR = '0xdac17f958d2ee523a2206206994597c13d831ec7'

  raw_pools = await get_pools(token0=USDC_TOKEN_ADDR, token1=USDT_TOKEN_ADDR)
  pools = parse_pools(raw_pools)

  graph_representation = create_graph_representation(pools)
  # print(graph_representation)
  G = create_approx_graph(graph_representation)
  draw_graph(G)

asyncio.run(main())