async function huy(file){
	try{
	process.env.GOOGLE_APPLICATION_CREDENTIALS = './test.json';
	const keys = require('./test.json')
	const vision = require('@google-cloud/vision');

	// Creates a client
	const client = new vision.ImageAnnotatorClient();

	/**
	 * TODO(developer): Uncomment the following line before running the sample.
	 */
	const fileName = file;

	// Performs landmark detection on the local file
	const [result] = await client.landmarkDetection(fileName)
	const landmarks = result.landmarkAnnotations;
	// console.log('Landmarks:');
	var out;
	landmarks.forEach(landmark => out = landmark.description);
	return out;
	// console.log(out);
	}
	catch (e){
		console.log(e,"error")
	}
}
async function run() {
  var inp ="test.jpeg";
  const [data] = await huy(inp);
  console.log(data); // will print your data
  return data;
}
// file ="test.jpeg"
// huy(file);