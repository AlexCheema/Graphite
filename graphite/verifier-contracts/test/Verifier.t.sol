// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console2} from "forge-std/Test.sol";
import {UltraVerifier} from "../src/NoCycle.sol";

contract VerifierTest is Test {
    UltraVerifier public verifier;

    function setUp() public {
        verifier = new UltraVerifier();
        // TODO: eito you need to pass the proof and publicInputs here
        verifier.verify(_proof, _publicInputs);
    }

    function test_Increment() public {
        verifier.increment();
        assertEq(verifier.number(), 1);
    }

    function testFuzz_SetNumber(uint256 x) public {
        verifier.setNumber(x);
        assertEq(verifier.number(), x);
    }
}
