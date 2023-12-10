use dep::std;

// Unfortunately, we get O(n^2) space & time complexity

struct Node {
    index: u8,
    value: u8,
    adj_list: [bool; n_nodes],
    edge_matrix: [u16; n_nodes],
}

global n_nodes: u8 = 10; 


struct Graph {
    nodes: [Node; n_nodes],
}


fn main(graph: pub Graph, u: pub Node) -> pub bool{

    let mut visited: [bool; n_nodes] = [false; n_nodes]; // Initialize visited array
    let mut tx_values: [u16; n_nodes] = [65535; n_nodes];

    // Simulating a queue with an array and head & tail 
    let mut queue: [(u8,u16); n_nodes] = [(0,0); n_nodes];
    let mut head = 0;
    let mut tail: Field = 1;
    let mut wash_trade = false;
    queue[head] = (u.index,0); 

    for _i in 0..10 {
        // Remote v_i from the queue
        let (current_index, current_value) = queue[head];
        head += 1;
        
        let current_node = graph.nodes[current_index];
        // Look at nodes connected to v_i, if not visited, add to queue
        for j in 0..10 {
            if current_node.adj_list[j] {
                let tx_value = current_node.edge_matrix[j];
                let next_value = tx_value + current_value;
                if  (!visited[j]) | (tx_values[j] > next_value) {

                    visited[j] = true;
                    
                    if (j == u.index) & (next_value > 0) {
                        wash_trade = true;
                    }

                    queue[tail] = (j as u8, next_value as u16);
                    tail += 1;
                }
            }


        }
    }
    wash_trade

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
            nodes[i] = Node { index: i as u8, 
                              value: 0 as u8, 
                              adj_list: [false; n_nodes], 
                              edge_matrix: [0; n_nodes] };
        } else {
            nodes[i] = Node { index: i as u8, 
                              value: (i+1) as u8, 
                              adj_list: [false; n_nodes], 
                              edge_matrix: [0; n_nodes] };
        }
    }

    nodes[0].adj_list = [false, true, false, false, false, false, false, false, false, false];
    nodes[1].adj_list = [false, false, true, true, false, false, false, false, false, false];


    let graph = Graph { nodes: nodes };
    let wash_trade = main(graph, nodes[0]);

    std::println("Hello Testing");
    std::println(wash_trade);

}
