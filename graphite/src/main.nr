use dep::std;

// Unfortunately, we get O(n^2) space & time complexity

struct Node {
    index: u8,
    value: u8,
    adj_list: [bool; n_nodes],
    edge_matrix: [u8; n_nodes],
}

global n_nodes: u8 = 10; 


struct Graph {
    nodes: [Node; n_nodes],
}


fn main(graph: pub Graph, u: pub Node) -> pub [u8; n_nodes]{

    let mut level: [u8; n_nodes] = [0; n_nodes]; // Initialize level array
    let mut visited: [bool; n_nodes] = [false; n_nodes]; // Initialize visited array

    // Simulating a queue with an array and head & tail 
    let mut queue: [u8; n_nodes] = [0; n_nodes];
    let mut head = 0;
    let mut tail: Field = 1;
    queue[head] = u.index;
    level[u.index as Field] = 1;


    for _i in 0..10 {
        // Remote v_i from the queue
        let v_i: Field = queue[head] as Field;
        head += 1;
        
        // Look at nodes connected to v_i, if not visited, add to queue
        for j in 0..10 {
            if graph.nodes[v_i].adj_list[j] & !visited[j] {
                queue[tail] = j as u8;
                level[j] = level[v_i] + 1;
                visited[j] = true;
                tail += 1;
            }
        }
    }

    level
}


#[test]
fn test_main() {

    let mut nodes: [Node; n_nodes] = [Node { index: 0, 
                                             value: 0, 
                                             adj_list: [false; n_nodes], 
                                             edge_matrix: [0; n_nodes] }
                                        ; n_nodes];

    for i in 0..10 {
        if i as u8 >= 3 {
            nodes[i] = Node { index: 0 as u8, 
                              value: i as u8, 
                              adj_list: [false; n_nodes], 
                              edge_matrix: [0; n_nodes] };
        } else {
            nodes[i] = Node { index: 0 as u8, 
                              value: i as u8, 
                              adj_list: [false; n_nodes], 
                              edge_matrix: [0; n_nodes] };
        }
    }

    let graph = Graph { nodes: nodes };
    let result = main(graph, nodes[0]);

    std::println(result[0]);
    assert(result[0] == 0);
    assert(result[1] == 1);

}
