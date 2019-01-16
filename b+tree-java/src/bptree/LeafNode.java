package bptree;

public class LeafNode extends Node {

	int M, N, index;
	int[][] P;
	LeafNode R;
	NonLeafNode up = null;
	NonLeafNode roofNode;
	
	public LeafNode()
	{
		this.M = 0;
		this.roofNode = new NonLeafNode(N);
	}
	
	public LeafNode(int N)
	{

		this.N = N;
		this.M = 0;
		this.roofNode = new NonLeafNode(N);
		this.P = new int[N][2];
	}
	
	public Node insertLeafKey(int key, int value)
	{
		if(M == N)
		{		
			//Find middle index to node split
			int middleIndex = 0;
			if(N % 2 == 0)
				middleIndex = N/2 - 1;
			else if(N % 2 == 1)
				middleIndex = N/2;
			
			LeafNode newNode = new LeafNode(N);
			//When key is inserted in new node
			if(P[middleIndex][0] < key)
			{
				for(int i = middleIndex + 1, j = M; i < j; i++)
				{
					//Move to new and initialize key in old node
					newNode.insertLeafKey(this.P[i][0], this.P[i][1]);
					this.P[i][0] = 0;
					this.P[i][1] = 0;
					M--;
				}
				newNode.insertLeafKey(key , value);
			}
			
			//When key is inserted in old node
			else
			{
				for(int i = middleIndex, j = M; i < j; i++)
				{
					//Move to new node and initialize key in old node
					newNode.insertLeafKey(this.P[i][0], this.P[i][1]);
					this.P[i][0] = 0;
					this.P[i][1] = 0;
					M--;
				}
				this.insertLeafKey(key, value);
			}
			
			
			if(up == null)
				this.up = new NonLeafNode(N);
		
			this.R = newNode;
			return up.insertNonLeafKey(newNode.P[0][0], this, newNode);
		}
		
		//Not leaf split. Just insert.
		else
		{
			//Find position to insert key
			for(index = 0; index < M && P[index][0] < key; index++);
			
			//When Position is last
			if(index >= M)
			{
				P[index][0] = key;
				P[index][1] = value;
				M++;
			}
			
			//When Position is not last
			else
			{
				for(int i = M-1; i >= index; i--)
				{
					//Push key, value backwards
					P[i+1][0] = P[i][0];
					P[i+1][1] = P[i][1];
				}
				
				P[index][0] = key;
				P[index][1] = value;
				M++;	
			}	
		}
		
		if(this.up == null)
			return this;
		
		else
		{
			roofNode = this.up;
			roofNode.up = this.up.up;
			while(roofNode.up != null)
				roofNode = roofNode.up;
		}
		
		return roofNode;
	}	
	
	public Node deleteLeafKey(int key)
	{
		int deleteKey = 0;
		
		//Find index where key exist
		for(index = 0; index < this.M && this.P[index][0] != key; index++);
		
		//Delete key and value from node
		if(index < this.M)
		{
			deleteKey = P[index][0];
			P[index][0] = 0;
			P[index][1] = 0;
		}	
		
		//Fill empty space of array
		for(int i = index; i < M - 1; i++)
		{
			//Push key, value forwards
			P[i][0] = P[i+1][0];
			P[i][1] = P[i+1][1];
			P[i+1][0] = 0;
			P[i+1][1] = 0;
		}
		M--;
		
		//If deleted key was located at the front of node, upper part of tree may have that key
		//So we have to change it
		if(this.up != null && index == 0)
			up.changeKey(deleteKey, this.P[0][0]);
		
		//When node has too few entries due to the removal
		if(M < N/2 && this.up != null)
		{
			//Find position at the upper node where child is
			int upIndex;
			for(upIndex = 0; upIndex < up.M && up.P[upIndex].key <= this.P[0][0]; upIndex++);
			
			//Find left and right sibling of the node
			LeafNode leftSibling = new LeafNode(N);
			LeafNode rightSibling = new LeafNode(N);
			
			if(upIndex > 0)
				leftSibling = ((LeafNode) up.P[upIndex-1].leftChildNode);
			if(upIndex < up.M)
				if(upIndex + 1 == ((NonLeafNode)up).M)
					rightSibling = ((LeafNode) up.R);
				else	
					rightSibling = ((LeafNode) up.P[upIndex+1].leftChildNode);
			
			//When node is not leftmost
			if(upIndex != 0)
			{	
				//Borrow key from left sibling
				if(((LeafNode)leftSibling).M - 1 >= N/2)
				{
					int borrowKey = leftSibling.P[leftSibling.M-1][0];
					int borrowValue = leftSibling.P[leftSibling.M-1][1];
				
					this.insertLeafKey(borrowKey, borrowValue);
					
					leftSibling.P[leftSibling.M - 1][0] = 0;
					leftSibling.P[leftSibling.M - 1][1] = 0;
					(leftSibling.M)--;
					
					up.changeKey(this.P[1][0], borrowKey);		
				}
				
				//When node is not rightmost child of up, borrow key from right sibling
				else if(upIndex < up.M && rightSibling.M -1 >= N/2)
				{
					int borrowKey = rightSibling.P[0][0];
					int borrowValue = rightSibling.P[0][1];
					int rightM = rightSibling.M;
					
					this.insertLeafKey(borrowKey, borrowValue);
					
					rightSibling.P[0][0] = 0;
					rightSibling.P[0][1] = 0;
					
					//Pull key forwards
					for(int i = 0; i < rightM - 1; i++)
					{
						rightSibling.P[i][0] = rightSibling.P[i+1][0];
						rightSibling.P[i][1] = rightSibling.P[i+1][1];
					}
					rightSibling.P[rightM - 1][0] = 0;
					rightSibling.P[rightM - 1][1] = 0;
					(rightSibling.M)--;
					
					up.changeKey(borrowKey, rightSibling.P[0][0]);		
				}
				
				//Merge with left sibling
				else
				{
					int leftM = ((LeafNode)leftSibling).M;
					int thisM = this.M;
					int upDeleteKey = this.P[0][0];
					
					//Insert key into back part of left sibling
					for(int i = 0; i < thisM; i++)
					{
						((LeafNode)leftSibling).P[i+leftM][0] = this.P[i][0];
						((LeafNode)leftSibling).P[i+leftM][1] = this.P[i][1];
						((LeafNode)leftSibling).M++;
						
						this.P[i][0] = 0;
						this.P[i][1] = 0;
						this.M--;
					}
					
					return up.deleteNonLeafKey(deleteKey);
				}
			}
			
			//When node is leftmost
			else if(upIndex == 0)
			{
				//Borrow key from right
				if(upIndex < up.M && rightSibling.M -1 >= N/2)
				{
					int borrowKey = rightSibling.P[0][0];
					int borrowValue = rightSibling.P[0][1];
					int rightM = rightSibling.M;
					
					this.insertLeafKey(borrowKey, borrowValue);
					
					rightSibling.P[0][0] = 0;
					rightSibling.P[0][1] = 0;
					for(int i = 0; i < rightM - 1; i++)
					{
						rightSibling.P[i][0] = rightSibling.P[i+1][0];
						rightSibling.P[i][1] = rightSibling.P[i+1][1];
					}
					rightSibling.P[rightM - 1][0] = 0;
					rightSibling.P[rightM - 1][1] = 0;
					(rightSibling.M)--;
					
					up.changeKey(borrowKey, rightSibling.P[0][0]);		
				}
				
				//Merge with right sibling
				else
				{
					int rightM = rightSibling.M;
					int thisM = this.M;
					int upDeleteKey = this.P[0][0];
					
					//Make space in right sibling for merge
					for(int i = rightM - 1; i >= 0; i--)
					{
						((LeafNode)rightSibling).P[i+thisM][0] = ((LeafNode)rightSibling).P[i][0];
						((LeafNode)rightSibling).P[i+thisM][1] = ((LeafNode)rightSibling).P[i][1];
					}
					
					//Insert original node into right sibling
					for(int i = 0; i < thisM; i++)
					{
						((LeafNode)rightSibling).P[i][0] = this.P[i][0];
						((LeafNode)rightSibling).P[i][1] = this.P[i][1];
						((LeafNode)rightSibling).M++;
						
						this.P[i][0] = 0;
						this.P[i][1] = 0;
						this.M--;
					}
					up.changeKey(rightSibling.P[thisM][0], rightSibling.P[0][0]);
					
					return up.deleteNonLeafKey(upDeleteKey);
				}
			}
		}
				
		if(this.up == null)
			return this;
			
		else
		{
			roofNode = this.up;
			roofNode.up = this.up.up;
			while(roofNode.up != null)
				roofNode = roofNode.up;
		}
			
		return roofNode;
	}
}