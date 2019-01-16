package bptree;

public class Node {

	int M, N, index;
	int[][] P;
	Node R;
	NonLeafNode up = null;
	Node roofNode;
	
	public Node()
	{
		this.up = null;
	}
	
	public Node insertLeafKey(int key, int value)
	{
		return new Node();
	}
	
	public Node insertNonLeafKey(int key, Node leftChildNode, Node rightChildNode)
	{
		return new Node();
	}
	
	public Node insertRoofDown(int key, int value)
	{
		return new Node();
	}
	public Node deleteLeafKey(int key)
	{
		return new Node();
	}
	public Node deleteRoofDown(int key)
	{
		return new Node();
	}
}