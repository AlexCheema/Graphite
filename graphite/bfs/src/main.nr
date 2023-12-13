use dep::std;

// Unfortunately, we get O(n^2) space & time complexity

struct Node<T, E, N> {
    index: u8,
    value: T,
    adj_list: [bool; N],
    edge_matrix: [E; N],
}

struct Graph<T, E, N> {
    nodes: [Node<T, E, N>; N],
}

fn bfs<T, E, N>(graph: Graph<T, E, N>, u: Node<T, E, N>) -> [u8; N]{

    let mut level: [u8; N] = [0; N]; // Initialize level array
    let mut visited: [bool; N] = [false; N]; // Initialize visited array

    // Simulating a queue with an array and head & tail
    let mut queue: [u8; N] = [0; N];
    let mut head = 0;
    let mut tail: Field = 1;
    queue[head] = u.index;
    level[u.index as Field] = 1;


    for _i in 0..graph.nodes.len() {
        // Remote v_i from the queue
        let v_i: Field = queue[head] as Field;
        head += 1;

        // Look at nodes connected to v_i, if not visited, add to queue
        for j in 0..graph.nodes.len() {
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

fn main(graph: pub Graph<u8, u8, 10>, u: pub Node<u8, u8, 10>) -> pub [u8; 10] {
    bfs(graph, u)
}



#[test]
fn test_bfs() {
    std::println("Hello Test");

    let mut nodes: [Node<u8, u8, 10>; 10] = [Node { index: 0,
                                             value: 0,
                                             adj_list: [false; 10],
                                             edge_matrix: [0; 10] }
                                        ; 10];

    for i in 0..10 {
        if i as u8 >= 3 {
            nodes[i] = Node { index: i as u8,
                              value: 0 as u8,
                              adj_list: [false; 10],
                              edge_matrix: [0; 10] };
        } else {
            nodes[i] = Node { index: i as u8,
                              value: (i+1) as u8,
                              adj_list: [false; 10],
                              edge_matrix: [0; 10] };
        }
    }

    nodes[0].adj_list = [false, true, false, false, false, false, false, false, false, false];
    nodes[1].adj_list = [false, false, true, true, false, false, false, false, false, false];

    let graph = Graph { nodes: nodes };

    std::println(nodes[0]);
    std::println(graph.nodes[0]);

    let result = bfs(graph, nodes[0]);

    std::println("Hello Testing");
    std::println(result[0]);
    std::println(result[1]);
    std::println(result[2]);
    std::println(result[3]);

    assert(result[0] == 1);
    assert(result[1] == 2);
    assert(result[2] == 3);
    assert(result[3] == 3);
}