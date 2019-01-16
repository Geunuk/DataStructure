package bptree;
import java.util.Scanner;
import java.io.PrintWriter;
import java.io.FileNotFoundException;
import java.io.FileInputStream;
import java.io.FileOutputStream;


public class BpTree {

	static Node roofNode = null;
	static LeafNode leaf = null;

	public static void main(String[] args)
	{
		PrintWriter outputStream = null;
		Scanner inputStream = null, inputIndexStream = null;
		int N=0;
	
		if(args[0].equals("-c"))
		{
			try {
				outputStream = new PrintWriter(new FileOutputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				System.exit(0);
				System.out.println("File not found");
			}
			
			N = Integer.parseInt(args[2]);
			outputStream.println(N);
			roofNode = new LeafNode(N);
			printIndex(outputStream, roofNode, N);
			outputStream.close();
		}
		
		else if(args[0].equals("-i"))
		{
			
			try {
				inputIndexStream = new Scanner(new FileInputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			
			N = inputIndexStream.nextInt();
			inputIndexStream.nextLine();
			
			roofNode = readIndex(inputIndexStream);
			if(roofNode instanceof LeafNode)
				N = ((LeafNode)roofNode).N;
			else if(roofNode instanceof LeafNode)
				N = ((NonLeafNode)roofNode).N;
			System.out.println(N);
			
			inputIndexStream.close();
			
			//Read insert file
			try {
				inputStream = new Scanner(new FileInputStream(args[2]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			
			while(inputStream.hasNext())
			{
				String insertLine = inputStream.nextLine();
				int commaIndex = insertLine.indexOf(",");
				int key = Integer.parseInt(insertLine.substring(0,  commaIndex));
				int value = Integer.parseInt(insertLine.substring(commaIndex + 1, insertLine.length()));
				
				
				//If this is your first insert, then roofNode must be null
				if(roofNode == null)
				{
					roofNode = new LeafNode(N);
					roofNode = roofNode.insertLeafKey(key, value);
				}
				
				else if(roofNode instanceof LeafNode)
					roofNode = roofNode.insertLeafKey(key, value);
				
				else if(roofNode instanceof NonLeafNode)
					roofNode = roofNode.insertRoofDown(key, value);
				
			}
			inputStream.close();
			
			try {
				outputStream = new PrintWriter(new FileOutputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				System.exit(0);
				System.out.println("File not found");
			}
			outputStream.println(N);
			printIndex(outputStream, roofNode, N);
			outputStream.close();
			
		}
		
		else if(args[0].equals("-d"))
		{
			try {
				inputStream = new Scanner(new FileInputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			N = Integer.parseInt(inputStream.nextLine());
			roofNode = readIndex(inputStream);
			inputStream.close();
			
			try {
				inputStream = new Scanner(new FileInputStream(args[2]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			
			while(inputStream.hasNextInt())
			{
				int key = Integer.parseInt(inputStream.nextLine());
				
				if(roofNode instanceof LeafNode)
					roofNode = roofNode.deleteLeafKey(key);
				
				else if(roofNode instanceof NonLeafNode)
					roofNode = roofNode.deleteRoofDown(key);
					
			}
			inputStream.close();
			
			try {
				outputStream = new PrintWriter(new FileOutputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				System.exit(0);
				System.out.println("File not found");
			}
			outputStream.println(N);
			printIndex(outputStream, roofNode, N);
			outputStream.close();			
		}
		
		
		else if(args[0].equals("-s"))
		{
			try {
				inputStream = new Scanner(new FileInputStream(args[1]));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			
			roofNode = readIndex(inputStream);
			inputStream.close();
			
			//Single key search
			if(args.length == 3)
			{
				int searchKey = Integer.parseInt(args[2]);
				
				if(roofNode instanceof LeafNode)
				{
					for(int i = 0; i < ((LeafNode) roofNode).M; i++)
					{
						if(((LeafNode)roofNode).P[i][0] == searchKey)
						{
							System.out.println(((LeafNode)roofNode).P[i][1]);
							break;
						}
					}
				}
				
				else if(roofNode instanceof NonLeafNode)
				{
					int index;
					
					while(!(roofNode instanceof LeafNode))
					{
						
						System.out.print(((NonLeafNode)roofNode).P[0].key);
						int M = ((NonLeafNode)roofNode).M;
						for(int i = 1; i < M; i++)
							System.out.print("," + ((NonLeafNode)roofNode).P[i].key);
						System.out.println();
						for(index = 0; index < M && ((NonLeafNode)roofNode).P[index].key <= searchKey; index++);
						if(index >= M)
							roofNode = ((NonLeafNode)roofNode).R;
						else
							roofNode = ((NonLeafNode)roofNode).P[index].leftChildNode;
					}
					
					for(index = 0; index < ((LeafNode) roofNode).M; index++)
					{
						if(((LeafNode)roofNode).P[index][0] == searchKey)
						{
							System.out.println(((LeafNode)roofNode).P[index][1]);
							break;
						}
					}
					if(index >= ((LeafNode) roofNode).M)
						System.out.println("NOT FOUND");
				}
			}
			
			//Ranged Search
			else if(args.length == 4)
			{
				int startKey = Integer.parseInt(args[2]);
				int endKey = Integer.parseInt(args[3]);
				
				if(roofNode instanceof LeafNode)
				{
					for(int i = 0; i < ((LeafNode) roofNode).M; i++)
					{
						if(startKey <= ((LeafNode)roofNode).P[i][0] && ((LeafNode)roofNode).P[i][0] <= endKey)
						{
							System.out.println(((LeafNode)roofNode).P[i][0] + "," + ((LeafNode)roofNode).P[i][1]);
						}
					}
				}
				
				else if(roofNode instanceof NonLeafNode)
				{
					int index;
					
					while(!(roofNode instanceof LeafNode))
					{
						int M = ((NonLeafNode)roofNode).M;
						
						for(index = 0; index < M && ((NonLeafNode)roofNode).P[index].key <= startKey; index++);
						if(index >= M)
							roofNode = ((NonLeafNode)roofNode).R;
						else
							roofNode = ((NonLeafNode)roofNode).P[index].leftChildNode;
					}
					
					int cnt = 0;
					while(((LeafNode)roofNode) != null && ((LeafNode)roofNode).P[0][0] < endKey)
					{
						for(index = 0; index < ((LeafNode) roofNode).M && ((LeafNode)roofNode).P[index][0] <= endKey; index++)
						{
							if(startKey <= ((LeafNode)roofNode).P[index][0])
							{
								System.out.println(((LeafNode)roofNode).P[index][0] + "," + ((LeafNode)roofNode).P[index][1]);
								cnt++;
							}
						}
						if(index >= ((LeafNode) roofNode).M )
							roofNode = roofNode.R;
						else
							break;
					}
					if(cnt == 0)
						System.out.println("NOT FOUND");
				}
			}	
		}	
	}
	
	public static void print(Node roofNode, int N)
	{
	
		if(roofNode instanceof NonLeafNode)
		{
			System.out.print("N" + " " + ((NonLeafNode) roofNode).M + " " + ((NonLeafNode) roofNode).N + " ");
			
			for(int i = 0; i < N; i++)
			{
				System.out.print(((NonLeafNode) roofNode).P[i].key + " ");
			}
			System.out.println();
			
			for(int i = 0; i < N; i++)
				print(((NonLeafNode) roofNode).P[i].leftChildNode, N);
			print(((NonLeafNode) roofNode).R, N);
		}
		
		else if(roofNode instanceof LeafNode)
		{
			System.out.print("L" + " " + ((LeafNode) roofNode).M + " " + ((LeafNode) roofNode).N + " ");
			
			for(int i = 0; i < N; i++)
			{
				System.out.print(((LeafNode) roofNode).P[i][0] + " " + ((LeafNode) roofNode).P[i][1] + " ");
			}
			System.out.println();
		}
		
	}
	
	
	public static void printIndex(PrintWriter outputStream, Node roofNode, int N)
	{
	
		if(roofNode instanceof NonLeafNode)
		{
			outputStream.print("N" + " " + ((NonLeafNode) roofNode).M + " " + ((NonLeafNode) roofNode).N + " ");
			
			for(int i = 0; i < N; i++)
			{
				outputStream.print(((NonLeafNode) roofNode).P[i].key + " ");
			}
			outputStream.println();
			
			for(int i = 0; i < N; i++)
				printIndex(outputStream, ((NonLeafNode) roofNode).P[i].leftChildNode, N);
			printIndex(outputStream, ((NonLeafNode) roofNode).R, N);
		}
		
		else if(roofNode instanceof LeafNode)
		{
			outputStream.print("L" + " " + ((LeafNode) roofNode).M + " " + ((LeafNode) roofNode).N + " ");
			
			for(int i = 0; i < N; i++)
			{
				outputStream.print(((LeafNode) roofNode).P[i][0] + " " + ((LeafNode) roofNode).P[i][1] + " ");
			}
			outputStream.println();
		}
		
	}
	
	public static Node readIndex(Scanner inputStream)
	{
		Node roofNode = null;
		String type;
		int M, N;
		if(inputStream.hasNext() == false)
			return null;
		
		type = inputStream.next();
		M = inputStream.nextInt();
		N = inputStream.nextInt();
		
		if(type.equals("N"))
		{
			int key;
			roofNode = new NonLeafNode(N);
			((NonLeafNode) roofNode).M = M;
			
			for(int i = 0; i < N; i++)
			{
				key = inputStream.nextInt();
				if(i < M)
					((NonLeafNode) roofNode).P[i].key = key;
			}
			
			for(int i = 0; i < M; i++)
			{
				((NonLeafNode) roofNode).P[i].leftChildNode = readIndex(inputStream);
				if(((NonLeafNode) roofNode).P[i].leftChildNode instanceof NonLeafNode)
					((NonLeafNode) ((NonLeafNode) roofNode).P[i].leftChildNode).up = ((NonLeafNode) roofNode);
				
				else if(((NonLeafNode) roofNode).P[i].leftChildNode instanceof LeafNode)
					((LeafNode) ((NonLeafNode) roofNode).P[i].leftChildNode).up = ((NonLeafNode) roofNode);
			}
			
			((NonLeafNode) roofNode).R = readIndex(inputStream);
			if(((NonLeafNode) roofNode).R instanceof NonLeafNode)	
				((NonLeafNode) ((NonLeafNode) roofNode).R).up = ((NonLeafNode) roofNode);
		
			else if(((NonLeafNode) roofNode).R instanceof LeafNode)
				((LeafNode) ((NonLeafNode) roofNode).R).up = ((NonLeafNode) roofNode);
			
			//Connect leaf node using R
			if(roofNode.R instanceof LeafNode)
			{	
				((LeafNode) ((NonLeafNode) roofNode).P[M-1].leftChildNode).R = ((LeafNode) ((NonLeafNode) roofNode).R);
				for(int i = M-2; i >= 0; i--)
					((LeafNode) ((NonLeafNode) roofNode).P[i].leftChildNode).R = ((LeafNode) ((NonLeafNode) roofNode).P[i+1].leftChildNode);
			}
			
			else
			{
				Node tmp1 = new NonLeafNode(((NonLeafNode) roofNode));
				Node tmp2 = new NonLeafNode(((NonLeafNode) roofNode));
				tmp1 = ((NonLeafNode) tmp1).R;
				tmp2 = ((NonLeafNode) tmp2).P[M-1].leftChildNode;
			
				while(!(tmp1 instanceof LeafNode))
					tmp1 = ((NonLeafNode) tmp1).P[0].leftChildNode;
				while(!(tmp2 instanceof LeafNode))
					tmp2 = ((NonLeafNode)tmp2).R;
				tmp2.R = tmp1;
				
				for(int i = (((NonLeafNode) roofNode).M)-2 ; i >= 0; i--)
				{
					Node tmp3 = new NonLeafNode(((NonLeafNode) roofNode));
					Node tmp4 = new NonLeafNode(((NonLeafNode) roofNode));
					
					tmp3 = ((NonLeafNode) tmp3).P[i+1].leftChildNode;
					tmp4 = ((NonLeafNode) tmp4).P[i].leftChildNode;
					
					while(!(tmp3 instanceof LeafNode))
						tmp3 = ((NonLeafNode) tmp3).P[0].leftChildNode;
					while(!(tmp4 instanceof LeafNode))
						tmp4 = ((NonLeafNode) tmp4).R;
					
					tmp4.R = tmp3;
				}		
			}
			return roofNode;
		}
		else if(type.equals("L"))
		{
			int key, value;
			roofNode = new LeafNode(N);
			
			((LeafNode) roofNode).M = M;
			
			for(int i = 0; i < N; i++)
			{	
				key = inputStream.nextInt();
				value = inputStream.nextInt();
				if(i < M)
				{
					((LeafNode) roofNode).P[i][0] = key;
					((LeafNode) roofNode).P[i][1] = value;	
				}
			}
			
			return roofNode;
		}
		
		return roofNode;
	}
}
