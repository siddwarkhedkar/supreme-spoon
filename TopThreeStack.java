class TopThreeStack{
	
	static int[] allElements = new int[20];
	static int index = 0;

	public static void pushElement(int incomingValue){

		if (index > allElements.length -1){
			System.out.println("Can't add element; skipping");
			return;
		} else {
			allElements[index] = incomingValue;
			System.out.println("New element added!");
			index ++;
		}

		System.out.println(" ");

	}

	public static int popElement(){

		int pop = -1;

		if (index == 0){
			System.out.println("Empty stack!");
		} else {
			pop =  allElements[index - 1];
			index --;
		}

		return pop;

	}

	public static void main(String[] args) {

		System.out.println(popElement());

		for(String arg: args){
			int incomingValue = Integer.parseInt(arg);
			pushElement(incomingValue);
		}

		for( int i = 0; i < 3; i++){
			System.out.println(popElement());
		}	

	}
}