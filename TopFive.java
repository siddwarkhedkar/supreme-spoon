class TopFive{
	
	// Assumption that incoming Timestamp is always biggest

	static int[] topFiveTimestamps = new int[5];

	public static void incomingTimestamp(int newTimestamp){

		for(int i = 4; i > 0; i --){
			topFiveTimestamps[i] = topFiveTimestamps[i - 1];
		}
		topFiveTimestamps[0] = newTimestamp;

		for(int output : topFiveTimestamps){
			System.out.println(output);
		}

		System.out.println(" ");
	}

	public static void main(String[] args) {
		
		for (String arg:args){
			int newTimestamp = Integer.parseInt(arg);
			incomingTimestamp(newTimestamp);
		}


	}
}