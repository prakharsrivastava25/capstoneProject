// import scrape from "./scrapeForDistrict"
// import states from "./States.json"
// var forEach = require('async-foreach').forEach;
var states = require('./States.json'); //with path
const scrape=require('./scrapeForDistrict')
// console.log(states)



/*states["states"].forEach((i)=>
console.log(i["state"]))*/
/*const s = async function (states){
	// await scrape.scrape("rohtak","haryana");
	// await scrape.scrape("baksa","assam");

	// for(int i=0; i++; )

	forEach(states["states"],a)

	/*states["states"].forEach( (i)=>async {
	i["districts"].forEach((j)=>{
		// console.log(j)
		await scrape.scrape(j,i["state"])
	});
})*/


async function fore(states){
	// console.log(states["states"][0])
	for (var i in states["states"]){
		// console.log(states[0])
		state=states["states"][i]
		console.log(state)
		for(const district in state["districts"]){
			await scrape.scrape(state["districts"][district],state["state"])
		}
	}
}
/*p=states["states"]
for (var key in p) {
    if (p.hasOwnProperty(key)) {
        console.log(key + " -> " + p[key]);
    }
}
*/
/*
async function a(item,index,arr){
	// console.log(item,index,arr)
	this.async(forEach(item["districts"],b))
}

async function b(item,index,arr){
	console.log(item,index,arr)
	await this.async(scrape.scrape(item,arr["state"]))
// console.log(a);
}*/


fore(states)