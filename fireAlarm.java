class FireAlarm{
			static int[] lastFiveTimestamps = new int[5];

	public static void addFireAlarm(int newTimestamp, int index){
		/*
		int i = 0;
		while (i < lastFiveTimestamps.length){
	
			if (newTimestamp > lastFiveTimestamps[i]){
				System.out.println("Recent Timestamp");
				for(int j = lastFiveTimestamps.length - 1; j > i; j--){
					lastFiveTimestamps[j] = lastFiveTimestamps[j - 1];
				}
				lastFiveTimestamps[i] = newTimestamp;
				System.out.println("Timestamps updated");
				break;
			} else {
				System.out.println("Not most recent, checking with other timestamps");
			}

			i ++;
		}

		for(int k = 0; k < lastFiveTimestamps.length; k++){
			System.out.println(lastFiveTimestamps[k]);
		}
		*/

		lastFiveTimestamps[index] = newTimestamp;
		for(int k = 0; k < lastFiveTimestamps.length; k++){
			System.out.println(lastFiveTimestamps[k]);
		}
		System.out.println("    ");
	}

	public static int getMinimumElementsIndex(){ 
		int minimumValue = lastFiveTimestamps[0];
		for(int a = 0; a < lastFiveTimestamps.length; a++){
			if (lastFiveTimestamps[a] < minimumValue) {
				minimumValue = lastFiveTimestamps[a];
			}
		}

		int minimumValueIndex = 0;
		while (minimumValue != lastFiveTimestamps[minimumValueIndex]){
			minimumValueIndex++ ;
		}

		return minimumValueIndex;
	}

	public static void main(String[] args) {

		for(String arg:args){
			int incomingFireAlarm = Integer.parseInt(arg);
			addFireAlarm(incomingFireAlarm, getMinimumElementsIndex());			
		}


	}
}