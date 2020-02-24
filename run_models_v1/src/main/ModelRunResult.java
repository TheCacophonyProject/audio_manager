package main;

public class ModelRunResult implements Comparable<ModelRunResult>{

	private String device_super_name;
	private String device_name;
	private double probability;
	private boolean used_to_create_model;
	private int recording_id;
	private double startTime;
	private String actual_confirmed;
	private String predictedByModel;
	private int month;
	private int year;
	
	
	
	// positive and negative are set depending on if actual_confirmed is a morepork.  They are the opposite of each other, so only need the one, but it is less confusing to do later calculations if have both
	private boolean positive = false;  
	private boolean negative = false;  // this can't stay this way !
	
	private int runningTotalPositives = 0;
	private int runningTotalNegatives = 0;
	
	private boolean truePositive = false;
	private int runningTotalTruePositives = 0;
	
	private boolean trueNegative = false;
	private int runningTotalTrueNegatives = 0;
	
	private boolean falsePositive = false;
	private int runningTotalFalsePositives = 0;
	
	private boolean falseNegative = false;
	private int runningTotalFalseNegatives = 0;
	
	private double truePositiveRate = 1; // would prefer this to be null but can't as it is a double
	
	private double coverageRate = 0;
	
	private double incorrectMoreporkPredictionRate = 0;
	
	private double falsePositveRateIfAlwaysPredictMorePork = 0; // ie no model
	

	public ModelRunResult(String device_super_name, String device_name, double probability, boolean used_to_create_model,
			int recording_id, double startTime, String actual_confirmed, String predictedByModel, int month, int year) {

		this.setDevice_super_name(device_super_name);
		this.setDevice_name(device_name);
		this.setProbability(probability);
		this.setUsed_to_create_model(used_to_create_model);
		this.setRecording_id(recording_id);
		this.setStartTime(startTime);
		this.setActual_confirmed(actual_confirmed);
		this.setPredictedByModel(predictedByModel);
		this.setMonth(month);
		this.setYear(year);
		
		setTrueFalses();

	}
	
	public void setTrueFalses() {
		if (getActual_confirmed().equalsIgnoreCase("morepork_more-pork")) {
			setPositive(true);
			setNegative(false);
		}else {
			setPositive(false);
			setNegative(true);
		}
		
		
		if (getPredictedByModel().equalsIgnoreCase("morepork_more-pork")) {	//  predicted positive		
			if (getActual_confirmed().equalsIgnoreCase("morepork_more-pork")) {
				setTruePositive(true);				
			}else {
				setFalsePositive(true);				
			}
		} else { //  predicted negative
			if (getActual_confirmed().equalsIgnoreCase("morepork_more-pork")) {
				setFalseNegative(true);
			}else {
				setTrueNegative(true);
			}
		}
	}

	public String toString() {
		return getDevice_super_name() + " " + getDevice_name() + " " + getProbability() + " " + isUsed_to_create_model() + " "
				+ getRecording_id() + " " + getStartTime() + " "
				+ getActual_confirmed() + " " + getPredictedByModel() + " " + getMonth() + " " + getYear() + " " +  isTruePositive()  + " " +  getRunningTotalTruePositives()  + " " +  isFalsePositive() + " " +   getRunningTotalFalsePositives()  + " " +  isFalseNegative()  + " " +  getRunningTotalFalseNegatives()  + " " +  isTrueNegative()  + " " +  getRunningTotalTrueNegatives();
	}
	
	public String dataToPlot() {
		return getProbability() + "," + truePositiveRate + "," + coverageRate + "," + incorrectMoreporkPredictionRate + "," + falsePositveRateIfAlwaysPredictMorePork;
	}

	boolean isTruePositive() {
		return truePositive;
	}

	void setTruePositive(boolean truePositive) {
		this.truePositive = truePositive;
	}

	boolean isTrueNegative() {
		return trueNegative;
	}

	void setTrueNegative(boolean trueNegative) {
		this.trueNegative = trueNegative;
	}

	boolean isFalsePositive() {
		return falsePositive;
	}

	void setFalsePositive(boolean falsePositive) {
		this.falsePositive = falsePositive;
	}

	boolean isFalseNegative() {
		return falseNegative;
	}

	void setFalseNegative(boolean falseNegative) {
		this.falseNegative = falseNegative;
	}

	int getRunningTotalTruePositives() {
		return runningTotalTruePositives;
	}

	void setRunningTotalTruePositives(int runningTotalTruePositives) {
		this.runningTotalTruePositives = runningTotalTruePositives;
	}

	int getRunningTotalTrueNegatives() {
		return runningTotalTrueNegatives;
	}

	void setRunningTotalTrueNegatives(int runningTotalTrueNegatives) {
		this.runningTotalTrueNegatives = runningTotalTrueNegatives;
	}

	int getRunningTotalFalsePositives() {
		return runningTotalFalsePositives;
	}

	void setRunningTotalFalsePositives(int runningTotalFalsePositives) {
		this.runningTotalFalsePositives = runningTotalFalsePositives;
	}

	int getRunningTotalFalseNegatives() {
		return runningTotalFalseNegatives;
	}

	void setRunningTotalFalseNegatives(int runningTotalFalseNegatives) {
		this.runningTotalFalseNegatives = runningTotalFalseNegatives;
	}

	double getTruePositiveRate() {
		return truePositiveRate;
	}

	void setTruePositiveRate(double truePositiveRate) {
		this.truePositiveRate = truePositiveRate;
	}

	int getRunningTotalPositives() {
		return runningTotalPositives;
	}

	void setRunningTotalPositives(int runningTotalPositives) {
		this.runningTotalPositives = runningTotalPositives;
	}

	int getRunningTotalNegatives() {
		return runningTotalNegatives;
	}

	void setRunningTotalNegatives(int runningTotalNegatives) {
		this.runningTotalNegatives = runningTotalNegatives;
	}

	boolean isPositive() {
		return positive;
	}

	void setPositive(boolean positive) {
		this.positive = positive;
	}

	boolean isNegative() {
		return negative;
	}

	void setNegative(boolean negative) {
		this.negative = negative;
	}

	double getCoverageRate() {
		return coverageRate;
	}

	void setCoverageRate(double coverageRate) {
		this.coverageRate = coverageRate;
	}

	double getIncorrectMoreporkPredictionRate() {
		return incorrectMoreporkPredictionRate;
	}

	void setIncorrectMoreporkPredictionRate(double incorrectMoreporkPredictionRate) {
		this.incorrectMoreporkPredictionRate = incorrectMoreporkPredictionRate;
	}

	double getFalsePositveRateIfAlwaysPredictMorePork() {
		return falsePositveRateIfAlwaysPredictMorePork;
	}

	void setFalsePositveRateIfAlwaysPredictMorePork(double falsePositveRateIfAlwaysPredictMorePork) {
		this.falsePositveRateIfAlwaysPredictMorePork = falsePositveRateIfAlwaysPredictMorePork;
	}

	@Override
	public int compareTo(ModelRunResult modelRunResult) { // didn't end or sorting so didn't use this
		// TODO Auto-generated method stub
		if (modelRunResult.getProbability() > getProbability()) {
			return 1;
		}else if (modelRunResult.getProbability() < getProbability()) {
			return -1;
		}else {
			return 0;
		}
	
	}

	String getDevice_super_name() {
		return device_super_name;
	}

	void setDevice_super_name(String device_super_name) {
		this.device_super_name = device_super_name;
	}

	String getDevice_name() {
		return device_name;
	}

	void setDevice_name(String device_name) {
		this.device_name = device_name;
	}

	double getProbability() {
		return probability;
	}

	void setProbability(double probability) {
		this.probability = probability;
	}

	boolean isUsed_to_create_model() {
		return used_to_create_model;
	}

	void setUsed_to_create_model(boolean used_to_create_model) {
		this.used_to_create_model = used_to_create_model;
	}

	int getRecording_id() {
		return recording_id;
	}

	void setRecording_id(int recording_id) {
		this.recording_id = recording_id;
	}

	double getStartTime() {
		return startTime;
	}

	void setStartTime(double startTime) {
		this.startTime = startTime;
	}

	String getActual_confirmed() {
		return actual_confirmed;
	}

	void setActual_confirmed(String actual_confirmed) {
		this.actual_confirmed = actual_confirmed;
	}

	String getPredictedByModel() {
		return predictedByModel;
	}

	void setPredictedByModel(String predictedByModel) {
		this.predictedByModel = predictedByModel;
	}

	int getMonth() {
		return month;
	}

	void setMonth(int month) {
		this.month = month;
	}

	int getYear() {
		return year;
	}

	void setYear(int year) {
		this.year = year;
	}
}
