import asyncio
from airstack.execute_query import AirstackClient
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
api_key = os.getenv('AIRSTACK_API_KEY')
api_client = AirstackClient(api_key=api_key)

query = """
query GetTokenTransfers {
  TokenTransfers(
    input: {
      filter: {
        _or: {
          from: { _eq: "eitomiyamura.eth" }
          to: { _eq: "eitomiyamura.eth" }
        }
      }
      blockchain: ethereum
      limit: 2
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

async def main():
    execute_query_client = api_client.create_execute_query_object(
        query=query)

    query_response = await execute_query_client.execute_query()
    print(query_response.data)

asyncio.run(main())