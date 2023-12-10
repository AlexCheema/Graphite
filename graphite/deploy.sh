#!/bin/bash

RPC_URL=""
VERIFIER_CONTRACT=""
PRIVATE_KEY=$(grep PRIVATE_KEY .env | cut -d '=' -f2)

while (( "$#" )); do
  case "$1" in
    --rpc-url)
      RPC_URL=$2
      shift 2
      ;;
    --verifier-contract)
      VERIFIER_CONTRACT=$2
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -*|--*=)
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
  esac
done

forge create --rpc-url $RPC_URL --private-key $PRIVATE_KEY contracts/$VERIFIER_CONTRACT:UltraVerifier --legacy
