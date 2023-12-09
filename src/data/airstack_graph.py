import asyncio
from airstack.execute_query import AirstackClient
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx
import os

load_dotenv()  # take environment variables from .env.
api_key = os.getenv('AIRSTACK_API_KEY')
api_client = AirstackClient(api_key=api_key)

async def get_token_transfers(addr):
  query = """
  query GetTokenTransfers {
    TokenTransfers(
      input: {
        filter: {
          _or: {
            from: { _eq: \"""" + addr + """\" }
            to: { _eq: \"""" + addr + """\" }
          }
        }
        blockchain: ethereum
        limit: 20
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

  execute_query_client = api_client.create_execute_query_object(
      query=query)

  query_response = await execute_query_client.execute_query()

  return query_response.data

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
  data = await get_token_transfers("eitomiyamura.eth")
  token_transfers = parse_token_transfers(data)
  USDC_TOKEN_ADDR = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
  usdc_token_transfers = [transfer for transfer in token_transfers if transfer['token_info']['address'] == USDC_TOKEN_ADDR]

  graph_representation = create_graph_representation(usdc_token_transfers)
  G = create_approx_graph(graph_representation)
  draw_graph(G)

asyncio.run(main())