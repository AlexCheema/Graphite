import asyncio
from airstack.execute_query import AirstackClient
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx
import os
import pickle

load_dotenv()  # take environment variables from .env.
api_key = os.getenv('AIRSTACK_API_KEY')
api_client = AirstackClient(api_key=api_key)


async def get_token_transfers(addresses, token_address=None):
    # Modify the query to accept multiple addresses and an optional token address
    query = """
    query GetTokenTransfers {
      TokenTransfers(
        input: {
          filter: {
            _and: [
              {
                _or: [
                  """ + ', '.join(f'{{from: {{ _eq: "{addr}" }} }}' for addr in addresses) + """,
                  """ + ', '.join(f'{{to: {{ _eq: "{addr}" }} }}' for addr in addresses) + """
                ]
              },
              """ + (f'{{token: {{address: {{ _eq: "{token_address}" }} }} }}' if token_address else '{}') + """
            ]
          }
          blockchain: ethereum
          limit: 5
          order: { blockTimestamp: DESC }
        }
      ) {
        TokenTransfer {
          amount
          formattedAmount
          blockTimestamp
          token {
            symbol
            name
            decimals
            address
          }
          from {
            addresses
          }
          to {
            addresses
          }
          type
        }
      }
    }
    """

    print("querying addresses", addresses)

    execute_query_client = api_client.create_execute_query_object(query=query)
    query_response = await execute_query_client.execute_query()
    return query_response.data

async def get_token_transfers_recursive(addresses, token_address=None, depth=3, visited=None):
    if visited is None:
        visited = set()

    if depth == 0:
        return []

    print("visited", visited)
    raw_transfers = []

    # Filter the addresses
    filtered_addresses = [addr for addr in addresses if addr.lower() not in visited]
    visited.update(addr.lower() for addr in filtered_addresses)

    # Query for all the filtered addresses together
    data = await get_token_transfers(filtered_addresses, token_address)

    if not data or 'TokenTransfers' not in data or 'TokenTransfer' not in data['TokenTransfers']:
      print('bad data', data)
      return raw_transfers

    raw_transfers.append(data)

    # Get 'to' addresses for the next recursive call
    to_addresses = [transfer['to']['addresses'][0] for transfer in data['TokenTransfers']['TokenTransfer']]
    raw_transfers.extend(await get_token_transfers_recursive(to_addresses, token_address, depth-1, visited))

    return raw_transfers

def parse_token_transfers(data):
  # Creating an intermediate data structure for token transfers
  token_transfers = []

  for transfer in data['TokenTransfers']['TokenTransfer']:
      from_address = transfer['from']['addresses'][0]
      to_address = transfer['to']['addresses'][0]
      amount = transfer['formattedAmount']
      token_info = transfer['token']

      # Adding the transfer information to the list
      token_transfers.append({
          'from': from_address,
          'to': to_address,
          'amount': amount,
          'token_info': token_info
      })

  return token_transfers

def create_graph_representation(token_transfers):
   # Creating an intermediate representation of the graph using a map
  graph_representation = {}

  for transfer in token_transfers:
      from_address = transfer['from']
      to_address = transfer['to']
      amount = transfer['amount']
      token_info = transfer['token_info']

      # Initialize the node if not already present
      if from_address not in graph_representation:
          graph_representation[from_address] = {}
      if to_address not in graph_representation:
          graph_representation[to_address] = {}

      # Adding transfer information to the graph
      if to_address in graph_representation[from_address]:
          # If the edge already exists, sum up the amount
          graph_representation[from_address][to_address]['amount'] += amount
      else:
          # Create a new edge with initial amount and token info
          graph_representation[from_address][to_address] = {
              'amount': amount,
              'token_info': token_info
          }

  return graph_representation

def create_approx_graph(graph_representation):
  # Creating a directed graph using the intermediate representation
  G = nx.DiGraph()

  # Iterating over the intermediate representation to create nodes and edges
  for from_address, transfers in graph_representation.items():
      for to_address, transfer_details in transfers.items():
          amount = transfer_details['amount']
          # token_info = transfer_details['token_info']  # This can be included if needed

          # Adding nodes
          if from_address not in G:
              G.add_node(from_address)
          if to_address not in G:
              G.add_node(to_address)

          # Adding an edge with the amount as weight
          if G.has_edge(from_address, to_address):
              G[from_address][to_address]['weight'] += amount
          else:
              G.add_edge(from_address, to_address, weight=amount)

  return G


def draw_graph(G):
  # Drawing the graph with a circular layout
  pos = nx.circular_layout(G)

  # Modifying node labels to show only the first 4 and last 4 characters of the address
  node_labels = {node: node[:6] + '...' + node[-4:] for node in G.nodes()}

  nx.draw(G, pos, with_labels=False, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
  nx.draw_networkx_labels(G, pos, labels=node_labels)

  edge_labels = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

  plt.title("Token Transfer Graph")
  plt.show()


async def main():
  USDC_TOKEN_ADDR = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
  USDT_TOKEN_ADDR = '0xdac17f958d2ee523a2206206994597c13d831ec7'

  raw_token_transfers = await get_token_transfers_recursive(["eitomiyamura.eth"], depth=3)
  token_transfers = [parse_token_transfers(data) for data in raw_token_transfers]
  # Flatten token_transfers
  token_transfers = [item for sublist in token_transfers for item in sublist]
  usdc_token_transfers = [transfer for transfer in token_transfers if transfer['token_info']['address'].lower() == USDC_TOKEN_ADDR.lower()]

  graph_representation = create_graph_representation(usdc_token_transfers)
  print(graph_representation)
  G = create_approx_graph(graph_representation)
  draw_graph(G)

  # Save a static file of the graph G
  with open("graph.gpickle", "wb") as f:
      pickle.dump(G, f)

asyncio.run(main())