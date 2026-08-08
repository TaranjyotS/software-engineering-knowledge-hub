/*
General Java Coding Practice

This file is a collection of independent Java interview exercises. Each exercise keeps the question statement directly in the
source file as a block comment before the corresponding implementation, matching the self-contained format used by the Python
exercises in this folder.
*/

package InterviewPrep.coding_questions;

import java.util.*;

public class java_coding_questions{
    public static void main(String[] args){
        System.out.println("Java coding questions tackled so far.");
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/* In Java, implement a non-directed, non-weighted, graph with nodes that can be identified by letters of the Latin alphabet.
Implement a method that would find path between two nodes and return it as a string. You can assume that the path always exists.
listPath("A","K") should return AGRK for graph [A-G-B-D-E-F ; G-R-K].
- Nodes are unique
- Parsing of the graph definition is not part of the exercise - you can hard code the graph data structure*/

class GraphPathFinder{

    private static Map<String, List<String>> graph = new HashMap<>();

    static{
        graph.put("A", Arrays.asList("G"));
        graph.put("G", Arrays.asList("A", "B", "R"));
        graph.put("B", Arrays.asList("G", "D"));
        graph.put("D", Arrays.asList("B", "F"));
        graph.put("E", Arrays.asList("D", "F"));
        graph.put("F", Arrays.asList("E"));
        graph.put("R", Arrays.asList("G", "K"));
        graph.put("K", Arrays.asList("R"));
    }

    public static String listPath(String start, String end){
        Set<String> visited = new HashSet<>();
        List<String> path = new ArrayList<>();

        if (dfs(start, end, visited, path)){
            return String.join("", path);
        }
        return "";
    }

    private static boolean dfs(String current, String end, Set<String> visited, List<String> path){
        visited.add(current);
        path.add(current);

        if (current.equals(end)) return true;

        for (String neighbor : graph.getOrDefault(current, Collections.emptyList())){
            if (!visited.contains(neighbor)){
                if (dfs(neighbor, end, visited, path)){
                    return true;
                }
            }
        }

        path.remove(path.size() - 1); // If path doesn't lead to target
        return false;
    }

    public static void main(String[] args){
        System.out.println((listPath("A", "K")));
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
