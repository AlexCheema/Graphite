// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BreadthFirstSearch {
    // Representing a simple graph using an adjacency list
    // where the key is the node, and the value is an array of neighbors.
    mapping(uint => uint[]) public graph;

    // Add edges to the graph
    function addEdge(uint from, uint to) public {
        graph[from].push(to);
    }

    // Perform BFS starting from a given node
    function bfs(uint startNode) public view returns (uint[] memory) {
        uint[] memory visited = new uint[](100); // Adjust size as needed
        uint[] memory queue = new uint[](100);   // Adjust size as needed
        uint head = 0;
        uint tail = 0;

        // Enqueue start node
        queue[tail++] = startNode;

        while (head < tail) {
            uint currentNode = queue[head++];
            visited[currentNode] = 1;

            // Process all neighbors
            for (uint i = 0; i < graph[currentNode].length; i++) {
                uint neighbor = graph[currentNode][i];
                if (visited[neighbor] == 0) {
                    queue[tail++] = neighbor;
                    visited[neighbor] = 1;
                }
            }
        }

        return queue; // Returns the order in which nodes were visited
    }
}
