const characterId = args[0];
const apiResponse = await Functions.makeHttpRequest({
  method: 'POST',
  url: `https://gateway-arbitrum.network.thegraph.com/api/56c79aa4c0aee0d175eab847b146f550/subgraphs/id/HUZDsRpEVP2AvzDCyzDHtdc64dyDxx8FQjzsmqSg4H3B`,
  data: {
    query: `
    {
    pools(first: 5, where:{ token0:"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" }) {
      id
    	liquidity
    	tick
    	sqrtPrice
      token0 {
        id
        name
        symbol
        decimals

      }
      token1 {
        id
        name
        symbol
        decimals
      }
    }
  }
    `
  }
});
if (apiResponse.error) {
    console.log(apiResponse)
  throw Error("Request failed");
}
const { data } = apiResponse;
return Functions.encodeString(data.name);
