package bptree;

public class NonLeafNode extends Node{
	
	int M, N, index;
	KeyChildArray[] P;
	Node R;
	NonLeafNode roofNode;
	NonLeafNode up = null;

	public NonLeafNode(int N)
	{
		this.N = N;
		this.M = 0;
		P = new KeyChildArray[N];
		for(int i = 0; i < N; i++)
			P[i] = new KeyChildArray();
	}
	
	public NonLeafNode(NonLeafNode original)
	{
		this.N = original.N;
		this.M = original.M;
		this.up = original.up;
		this.R = original.R;
		this.P = new KeyChildArray[N];
		for(int i = 0; i < N; i++)
		{
			this.P[i] = new KeyChildArray();
			this.P[i].key = original.P[i].key;
			this.P[i].leftChildNode = original.P[i].leftChildNode;
		}
	}
	
	//Function that go down from top to the leaf and connect to the insertLeafKey
	public Node insertRoofDown(int key, int value)
	{
		Node result = new Node();
		
		for(index = 0; index < M && this.P[index].key < key; index++);
			
		//When Position is last
		if(index >= M)
		{
			if(R instanceof NonLeafNode)
				result = ((NonLeafNode) R).insertRoofDown(key, value);

			else if(R instanceof LeafNode)
				result = ((LeafNode) R).insertLeafKey(key, value);	
		}
		
		//When Position is not last
		else
		{
			Node down = P[index].leftChildNode;
			if(down instanceof NonLeafNode)
				result = ((NonLeafNode) down).insertRoofDown(key, value);
	
			else if(down instanceof LeafNode)
				result = ((LeafNode) down).insertLeafKey(key, value);	
		}
	
		return result;
	}
	
	public Node insertNonLeafKey(int key, Node leftChildNode, Node rightChildNode)
	{
		if(M == N)
		{		
			//Find middle index to node split
			int upIndex = 0;
			int upKey = 0;
			int middleIndex = 0;
			if(N % 2 == 0)
				middleIndex = N/2 - 1;
			else if(N % 2 == 1)
				middleIndex = N/2;
			
			NonLeafNode newNode = new NonLeafNode(N);
			
			//Insert key in new node
			if(P[middleIndex].key < key)
			{	
				//Move key to new node
				for(int i = middleIndex + 2, j = M; i < j; i++)
				{
					Node right;
					if(i + 1 == N)
						right = R;
					else
						right = this.P[i+1].leftChildNode;
					
					newNode.insertNonLeafKey(this.P[i].key, this.P[i].leftChildNode.roofNode, right);
				}
				
				//When insert key go up again, it must be handled separately
				if(key < P[middleIndex + 1].key )
				{
					Node right;
					if(middleIndex + 2 == N)
						right = R;
					else
						right = this.P[middleIndex + 2].leftChildNode;
					
					upKey = key;
					newNode.insertNonLeafKey(P[middleIndex + 1].key , leftChildNode, right);
					
					for(int i = middleIndex + 2, j = M; i < j; i++)
					{
						this.P[i].key = 0;
						this.P[i].leftChildNode = null;
						M--;
					}
					
					this.P[middleIndex + 1].key = 0;
					this.P[middleIndex + 1].leftChildNode = null;
					M--;
				}
				
				//When insert key did not go up again
				else
				{	
					for(int i = middleIndex + 2, j = M; i < j; i++)
					{
						this.P[i].key = 0;
						this.P[i].leftChildNode = null;
						M--;
					}
					
					upIndex = middleIndex + 1;
					upKey = P[middleIndex + 1].key;
					newNode.insertNonLeafKey(key , leftChildNode, rightChildNode);
				}
			}
			
			//Insert key in old node
			else
			{	
				//Move key to new node
				for(int i = middleIndex + 1, j = M; i < j; i++)
				{	
					Node right;
					if(i + 1 == N)
						right = R;
					else
						right = this.P[i+1].leftChildNode;
					
					newNode.insertNonLeafKey(this.P[i].key, this.P[i].leftChildNode, right);
					
					this.P[i].key = 0;
					this.P[i].leftChildNode = null;
					M--;
				}
				
				upIndex = middleIndex;
				upKey = P[middleIndex].key;	
			}
	
			if(up == null)
				up = new NonLeafNode(N);
			
			up.R = newNode;
			newNode.up = (NonLeafNode)up;
			
			//when insert key go up again
			if(upKey == key)
			{	
				newNode.R = this.R;
				
				this.R = leftChildNode;
				if(R instanceof NonLeafNode)
					((NonLeafNode) this.R).up = this;
				else if(R instanceof LeafNode)
					((LeafNode) this.R).up = this;
			
				newNode.P[0].leftChildNode = rightChildNode;
				if(newNode.P[0].leftChildNode instanceof NonLeafNode)
					((NonLeafNode) newNode.P[0].leftChildNode).up = newNode;
				else if(newNode.P[0].leftChildNode instanceof LeafNode)
					((LeafNode) newNode.P[0].leftChildNode).up = newNode;	
			}
			
			else
			{
				this.R = P[upIndex].leftChildNode;
				
				if(R instanceof NonLeafNode)
					((NonLeafNode) this.R).up = this;
				else if(R instanceof LeafNode)
					((LeafNode) this.R).up = this;
				
				if(newNode.P[0].leftChildNode instanceof NonLeafNode)
					((NonLeafNode) newNode.P[0].leftChildNode).up = newNode;
				else if(newNode.P[0].leftChildNode instanceof LeafNode)
					((LeafNode) newNode.P[0].leftChildNode).up = newNode;
				
				this.P[upIndex].key = 0;
				this.P[upIndex].leftChildNode = null;
				M--;
				
				if(upKey > key)
				{
				
					this.insertNonLeafKey(key, leftChildNode, rightChildNode);
				}
			}
			
			return up.insertNonLeafKey(upKey, this, newNode);
		}
		
		//Not nonLeaf split. Just insert.
		else
		{
			//Find position to insert key
			for(index = 0; index < M && P[index].key < key; index++); 

			//When Position is last
			if(index >= M)
			{
				P[index].key = key;
				P[index].leftChildNode = leftChildNode;
				
				if(P[index].leftChildNode instanceof LeafNode)
					((LeafNode) P[index].leftChildNode).up = this;
				
				else if(R instanceof NonLeafNode)
					((NonLeafNode) P[index].leftChildNode).up = this;
					
				this.R = rightChildNode;
				
				if(R instanceof LeafNode)
					((LeafNode) R).up = this;
				
				else if(R instanceof NonLeafNode)
					((NonLeafNode) R).up = this;
				
				M++;
			}
			
			//When Position is not last
			else
			{
				//Push key, value backwards
				for(int i = M-1; i >= index; i--)
				{
					P[i+1].key = P[i].key;
					P[i+1].leftChildNode = P[i].leftChildNode;
				}
				
				P[index].key = key;
				P[index].leftChildNode = leftChildNode;
				
				if(P[index].leftChildNode instanceof LeafNode)
					((LeafNode) P[index].leftChildNode).up = this;
	
				else if(P[index].leftChildNode instanceof NonLeafNode)
					((NonLeafNode) P[index].leftChildNode).up = this;
				
				P[index+1].leftChildNode = rightChildNode;
				if(P[index+1].leftChildNode instanceof LeafNode)
					((LeafNode) P[index+1].leftChildNode).up = this;
				
				else if(P[index+1].leftChildNode instanceof NonLeafNode)
					((NonLeafNode) P[index+1].leftChildNode).up = this;
				
				M++;	
			}
		}
		
		roofNode = this;
		roofNode.up = this.up;
		
		while(roofNode.up != null)
			roofNode = roofNode.up;
		
		return roofNode;
	}
	
	//Function that go down from top to the leaf and connect to the insertLeafKey
	public Node deleteRoofDown(int key)
	{
		Node result = new Node();
		
		for(index = 0; index < M && this.P[index].key <= key; index++);
		
		//When Position is last
		if(index >= M)
		{
			if(R instanceof NonLeafNode)		
				result = ((NonLeafNode) R).deleteRoofDown(key);

			else if(R instanceof LeafNode)
				result = ((LeafNode) R).deleteLeafKey(key);
			
		}
			
		//When Position is not last
		else
		{
			Node down = P[index].leftChildNode;
			
			if(down instanceof NonLeafNode)	
				result = ((NonLeafNode) down).deleteRoofDown(key);
			
			else if(down instanceof LeafNode)	
				result = ((LeafNode) down).deleteLeafKey(key);
			
		}
		
		return result;
	}
	
	public Node deleteNonLeafKey(int key)
	{
		int deleteKey = 0;
		
		//Find index where key exist
		for(index = 0; index < this.M && this.P[index].key < key; index++);
		
		if(this.up == null  && P[1].key == 0)
		{	
			if(this.P[0].leftChildNode instanceof LeafNode)
			{
				if(((LeafNode)this.P[0].leftChildNode).P[0][0] == 0)
				{
					((LeafNode)this.R).up = null;
					return this.R;
				}
				
				else if(((LeafNode)this.R).P[0][0] == 0)
				{
					((LeafNode)this.P[0].leftChildNode).up = null;
					return this.P[0].leftChildNode;
				}
			}
			
			else if(P[0].leftChildNode instanceof NonLeafNode)
			{
				if(((NonLeafNode)this.P[0].leftChildNode).P[0].key == 0)
				{
					((NonLeafNode)this.R).up = null;
					return this.R;	
				}
				
				else if(((NonLeafNode)this.R).P[0].key == 0)
				{
					((NonLeafNode)this.P[0].leftChildNode).up = null;
					return this.P[0].leftChildNode;
				}
				
			}
		}
		
		//Delete key and value from node
		if(index == 0)
		{	
			if(P[0].leftChildNode instanceof LeafNode && ((LeafNode) P[0].leftChildNode).P[0][0] == 0)
			{	
				((LeafNode)P[0].leftChildNode).up = null;
				P[0].leftChildNode = null;
				P[0].key = 0;
					
				for(int i = 0; i < M - 1; i++)
				{	
					System.out.println(P[i].key + " " + P[i+1].key);
					P[i].key = P[i+1].key;
					P[i].leftChildNode = P[i+1].leftChildNode;
					System.out.println(P[i].key + " " + P[i+1].key);	
				}
				
				P[M-1].key = 0;
				P[M-1].leftChildNode = null;
				M--;
			}
			
			else if(P[0].leftChildNode instanceof NonLeafNode && ((NonLeafNode) P[0].leftChildNode).P[0].key == 0)
			{
				((NonLeafNode)P[0].leftChildNode).up = null;
				P[0].leftChildNode = null;
				P[0].key = 0;
					
				for(int i = 0; i < M - 1; i++)
				{
					P[i].key = P[i+1].key;
					P[i].leftChildNode = P[i+1].leftChildNode;
				}
				
				P[M-1].key = 0;
				P[M-1].leftChildNode = null;
				M--;
			}
			
			else
			{	
				deleteKey = P[index].key;
				P[index].key = 0;
					
				if(index+1 == M)
				{
					if(R instanceof LeafNode)
						((LeafNode)this.R).up = null;
					
					else if(R instanceof NonLeafNode)
						((NonLeafNode)this.R).up = null;
					
					this.R = null;
					this.R = P[M-1].leftChildNode;
					M--;
				}
				
				else
				{
					if(P[index+1].leftChildNode instanceof LeafNode)
						((LeafNode)P[index+1].leftChildNode).up = null;
					
					else if(P[index+1].leftChildNode instanceof NonLeafNode)
						((NonLeafNode)P[index+1].leftChildNode).up = null;
					
					P[index+1].leftChildNode = null;
					P[index].key = P[index+1].key;
					
					for(int i = index + 1; i < M - 1; i++)
					{
						P[i].key = P[i+1].key;
						P[i].leftChildNode = P[i+1].leftChildNode;
					}
					
					P[M-1].key = 0;
					P[M-1].leftChildNode = null;
					M--;
				}
			}
				
		}
		
		else if(index < this.M)
		{	
			deleteKey = P[index].key;
			P[index].key = 0;
			
			if(index+1 == M)
			{
				if(R instanceof LeafNode)
					((LeafNode)this.R).up = null;
				
				else if(R instanceof NonLeafNode)
					((NonLeafNode)this.R).up = null;
				
				this.R = null;
				this.R = P[M-1].leftChildNode;
				M--;
			}
			
			else
			{
				if(P[index+1].leftChildNode instanceof LeafNode)
					((LeafNode)P[index+1].leftChildNode).up = null;
				
				else if(P[index+1].leftChildNode instanceof NonLeafNode)
					((NonLeafNode)P[index+1].leftChildNode).up = null;
				
				P[index+1].leftChildNode = null;
				P[index].key = P[index+1].key;
				
				for(int i = index + 1; i < M - 1; i++)
				{
					P[i].key = P[i+1].key;
					P[i].leftChildNode = P[i+1].leftChildNode;
				}
				
				P[M-1].key = 0;
				P[M-1].leftChildNode = null;
				M--;
			}
		}
		
		if(this.up != null && index == 0)
			up.changeKey(deleteKey, this.P[0].key);
		
		//When node has too few entries due to the removal
		if(M < N/2 && this.up != null)
		{
			int upIndex;
			
			for(upIndex = 0; upIndex < up.M && up.P[upIndex].key < this.P[0].key; upIndex++);
			
			NonLeafNode leftSibling = new NonLeafNode(N);
			NonLeafNode rightSibling = new NonLeafNode(N);
			
			if(upIndex > 0)
				leftSibling = ((NonLeafNode) up.P[upIndex-1].leftChildNode);
			
			if(upIndex < up.M)
				if(upIndex + 1 == ((NonLeafNode)up).M)
					rightSibling = ((NonLeafNode) up.R);
				else	
					rightSibling = ((NonLeafNode) up.P[upIndex+1].leftChildNode);
			
			//When node is not leftmost
			if(upIndex != 0)
			{	
				//Borrow key from left sibling
				if(leftSibling.M - 1 >= N/2)
				{
					int borrowKey = 0;
					
					Node borrowRightChild = leftSibling.R;
					Node tmp1 = new NonLeafNode(this);
					
					while(!(tmp1 instanceof LeafNode))
						tmp1 = ((NonLeafNode)tmp1).P[0].leftChildNode;
					
					int oldSmallestKey = ((LeafNode)tmp1).P[0][0];
					
					if(this.P[0].leftChildNode instanceof LeafNode)
						borrowKey = ((LeafNode)this.P[0].leftChildNode).P[0][0];
					
					else if(this.P[0].leftChildNode instanceof NonLeafNode)
						borrowKey = ((NonLeafNode)this.P[0].leftChildNode).P[0].key;
					
					for(int i = this.M - 1; i >= 0; i--)
					{
						this.P[i+1].key = this.P[i].key;
						this.P[i+1].leftChildNode = this.P[i].leftChildNode;
					}
					
					this.P[0].key = borrowKey;
					this.P[0].leftChildNode = borrowRightChild;
					
					if(this.P[0].leftChildNode instanceof LeafNode)
						((LeafNode)this.P[0].leftChildNode).up = this;
					
					if(this.P[0].leftChildNode instanceof NonLeafNode)
						((NonLeafNode)this.P[0].leftChildNode).up = this;
					
					this.M++;
					
					leftSibling.R = leftSibling.P[leftSibling.M-1].leftChildNode;
					leftSibling.P[leftSibling.M-1].key = 0;
					leftSibling.P[leftSibling.M-1].leftChildNode = null;
					(leftSibling.M)--;
									
					Node tmp2 = new NonLeafNode(this);
					while(!(tmp2 instanceof LeafNode))
						tmp2 = ((NonLeafNode)tmp2).P[0].leftChildNode;
					
					int newSmallestKey = ((LeafNode)tmp2).P[0][0];
					
					up.changeKey(oldSmallestKey, newSmallestKey);
				}
				
				//When node is Not R of up, borrow key from right sibling
				else if(upIndex < up.M && rightSibling.M -1 >= N/2)
				{
					int borrowKey = 0;
					
					Node borrowLeftChild = rightSibling.P[0].leftChildNode;
					
					if(rightSibling.R instanceof LeafNode)
						borrowKey = ((LeafNode)rightSibling.P[0].leftChildNode).P[0][0];
					
					else if(leftSibling.R instanceof NonLeafNode)
						borrowKey = ((NonLeafNode)rightSibling.P[0].leftChildNode).P[0].key;
					
					this.P[M].key = borrowKey;
					this.P[M].leftChildNode = this.R;
					this.R = borrowLeftChild;
					
					if(this.R instanceof LeafNode)
						((LeafNode)this.R).up = this;
					if(this.R instanceof NonLeafNode)
						((NonLeafNode)this.R).up = this;
					this.M++;
						
					rightSibling.P[0].key = 0;
					rightSibling.P[0].leftChildNode = null;
					
					for(int i = 0; i < rightSibling.M - 1; i++)
					{
						rightSibling.P[i].key = rightSibling.P[i+1].key;
						rightSibling.P[i].leftChildNode = rightSibling.P[i+1].leftChildNode;
					}
					
					rightSibling.P[rightSibling.M-1].key = 0;
					rightSibling.P[rightSibling.M-1].leftChildNode = null;
					(rightSibling.M)--;
					
					int newUpKey = 0;
					
					if(rightSibling.P[0].leftChildNode instanceof LeafNode)
						newUpKey = ((LeafNode)rightSibling.P[0].leftChildNode).P[0][0];
					
					else if(rightSibling.P[0].leftChildNode instanceof NonLeafNode)
						newUpKey = ((NonLeafNode)rightSibling.P[0].leftChildNode).P[0].key;
					
					up.changeKey(borrowKey, newUpKey);
				}
				
				//Merge with left sibling
				else
				{
					int leftM = ((NonLeafNode)leftSibling).M;
					int thisM = this.M;
					int upDeleteKey = this.up.P[0].key;
					
					for(int i = 0; i < thisM; i++)
					{
						((NonLeafNode)leftSibling).P[i+leftM+1].key = this.P[i].key;
						((NonLeafNode)leftSibling).P[i+leftM+1].leftChildNode = this.P[i].leftChildNode;
						
						if(((NonLeafNode)leftSibling).P[i+leftM+1].leftChildNode instanceof LeafNode)
							((LeafNode)((NonLeafNode)leftSibling).P[i+leftM+1].leftChildNode).up = leftSibling;
						
						else if(((NonLeafNode)leftSibling).P[i+leftM+1].leftChildNode instanceof NonLeafNode)
							((NonLeafNode)((NonLeafNode)leftSibling).P[i+leftM+1].leftChildNode).up = leftSibling;
						
						((NonLeafNode)leftSibling).M++;
					
						
						this.P[i].key = 0;
						this.P[i].leftChildNode = null;
						this.M--;
					}
					
					((NonLeafNode)leftSibling).P[leftM].key = this.up.P[upIndex].key;
					((NonLeafNode)leftSibling).P[leftM].leftChildNode = ((NonLeafNode)leftSibling).R;
					
					if(((NonLeafNode)leftSibling).P[leftM].leftChildNode instanceof LeafNode)
						((LeafNode)((NonLeafNode)leftSibling).P[leftM].leftChildNode).up = leftSibling;
					
					else if(((NonLeafNode)leftSibling).P[leftM].leftChildNode instanceof NonLeafNode)
						((NonLeafNode)((NonLeafNode)leftSibling).P[leftM].leftChildNode).up = leftSibling;
					
					
					((NonLeafNode)leftSibling).R = this.R;
					
					if(((NonLeafNode)leftSibling).R instanceof LeafNode)
						((LeafNode)((NonLeafNode)leftSibling).R).up = leftSibling;
					
					else if(((NonLeafNode)leftSibling).R instanceof NonLeafNode)
						((NonLeafNode)((NonLeafNode)leftSibling).R).up = leftSibling;
					
					((NonLeafNode)leftSibling).M++;
					
					return up.deleteNonLeafKey(upDeleteKey);
				}
			}
			
			//When node is leftmost
			else if(upIndex == 0)
			{
				
				//When node is Not R of up, borrow key from right
				if(upIndex < up.M && rightSibling.M -1 >= N/2)
				{
					int borrowKey = 0;
					
					Node borrowLeftChild = rightSibling.P[0].leftChildNode;
					
					if(rightSibling.R instanceof LeafNode)
						borrowKey = ((LeafNode)rightSibling.P[0].leftChildNode).P[0][0];
					
					else if(leftSibling.R instanceof NonLeafNode)
						borrowKey = ((NonLeafNode)rightSibling.P[0].leftChildNode).P[0].key;
					
					this.P[M].key = borrowKey;
					this.P[M].leftChildNode = this.R;
					
					this.R = borrowLeftChild;
					if(this.R instanceof LeafNode)
						((LeafNode)this.R).up = this;
					
					else if(this.R instanceof NonLeafNode)
						((NonLeafNode)this.R).up = this;
					
					this.M++;
					
					
					rightSibling.P[0].key = 0;
					rightSibling.P[0].leftChildNode = null;
					
					for(int i = 0; i < rightSibling.M - 1; i++)
					{
						rightSibling.P[i].key = rightSibling.P[i+1].key;
						rightSibling.P[i].leftChildNode = rightSibling.P[i+1].leftChildNode;
					}
					
					rightSibling.P[rightSibling.M-1].key = 0;
					rightSibling.P[rightSibling.M-1].leftChildNode = null;
					(rightSibling.M)--;
					
					int newUpKey = 0;
					
					if(rightSibling.P[0].leftChildNode instanceof LeafNode)
						newUpKey = ((LeafNode)rightSibling.P[0].leftChildNode).P[0][0];
					
					if(rightSibling.P[0].leftChildNode instanceof NonLeafNode)
						newUpKey = ((NonLeafNode)rightSibling.P[0].leftChildNode).P[0].key;
					
					up.changeKey(borrowKey, newUpKey);
				}
				
				//Merge with right sibling
				else
				{
					int rightM = ((NonLeafNode)rightSibling).M;
					int thisM = this.M;
					int oldRightFirstKey = ((NonLeafNode)rightSibling).P[0].key;
					int upDeleteKey = this.P[0].key;
					
					Node tmp1 = new NonLeafNode(rightSibling);
					while(!(tmp1 instanceof LeafNode))
						tmp1 = ((NonLeafNode)tmp1).P[0].leftChildNode;
				
					int oldSmallestKey = ((LeafNode)tmp1).P[0][0];
					
					for(int i = rightM -1; i >= 0; i--)
					{
						((NonLeafNode)rightSibling).P[i+thisM +1].key = ((NonLeafNode)rightSibling).P[i].key;
						((NonLeafNode)rightSibling).P[i+thisM + 1].leftChildNode = ((NonLeafNode)rightSibling).P[i].leftChildNode;
					}
					
					for(int i = 0; i < thisM; i++)
					{
						((NonLeafNode)rightSibling).P[i].key = this.P[i].key;
						((NonLeafNode)rightSibling).P[i].leftChildNode = this.P[i].leftChildNode;
						
						if(((NonLeafNode)rightSibling).P[i].leftChildNode instanceof LeafNode)
							((LeafNode)((NonLeafNode)rightSibling).P[i].leftChildNode).up = rightSibling;
						
						else if(((NonLeafNode)rightSibling).P[i].leftChildNode instanceof NonLeafNode)
							((NonLeafNode)((NonLeafNode)rightSibling).P[i].leftChildNode).up = rightSibling;
						
						((NonLeafNode)rightSibling).M++;
						
						this.P[i].key = 0;
						this.P[i].leftChildNode = null;
						this.M--;
					}
					
					((NonLeafNode)rightSibling).P[thisM].key = up.P[upIndex].key;
					((NonLeafNode)rightSibling).P[thisM].leftChildNode = this.R;
					
					if(((NonLeafNode)rightSibling).P[thisM].leftChildNode instanceof LeafNode)
						((LeafNode)((NonLeafNode)rightSibling).P[thisM].leftChildNode).up = rightSibling;
					
					else if(((NonLeafNode)rightSibling).P[thisM].leftChildNode instanceof NonLeafNode)
						((NonLeafNode)((NonLeafNode)rightSibling).P[thisM].leftChildNode).up = rightSibling;
					
					((NonLeafNode)rightSibling).M++;
					
					Node tmp2 = new NonLeafNode(rightSibling);
					while(!(tmp2 instanceof LeafNode))
						tmp2 = ((NonLeafNode)tmp2).P[0].leftChildNode;
					
					int newSmallestKey = ((LeafNode)tmp2).P[0][0];
					
					up.changeKey(oldSmallestKey, newSmallestKey);
					up.changeKey(oldRightFirstKey, rightSibling.P[0].key);	
					
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
	
	public void changeKey(int oldKey, int newKey)
	{
		NonLeafNode roof = this;
		
		while(roof != null)
		{	
			for(int i = 0; i < roof.M; i++)
			{
				if(roof.P[i].key == oldKey)
				{
					roof.P[i].key = newKey;
				}
			}
			roof = roof.up;
		}
	}
}