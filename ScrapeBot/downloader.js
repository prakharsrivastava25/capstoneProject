var download = require('download-file');
const fs = require('fs');

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

var checkUpper = (character) => {
	if (character == character.toUpperCase()) {
		 return true;
	}
	if (character == character.toLowerCase()){
		return false;
	}
}
var myArgs = process.argv.slice(2);
console.log(5*myArgs[0])
x=myArgs;
for(i=x*5;i<5+x*5;i++){
fileName='./urls/url'+i.toString()+'.json';
var obj = JSON.parse(fs.readFileSync(fileName, 'utf8')); 
obj.forEach((i)=>{
	i.title=i.title.split(" ");	
	x=8;
	state=[];district=[];

	while(true)
	if(checkUpper(i.title[x])) {
		district.push(i.title[x])
		x=x+1;
	}
	else {if(x==8) {district.push(i.title[8]);x=10;} break;}

	while(true)
	if(checkUpper(i.title[x+2])) {
		state.push(i.title[x+2])
		x=x+1;
	}
	else break;

	state=state.join(" ");district=district.join(" ");
	month=i.title[i.title.length-2];
	// console.log(i.title,month)
	file=district+" "+month;
	// console.log("state=",state,"district=",district);
	options = {
    directory: "./MonthwiseData/"+state+"/",
    filename: file+".csv",
    timeout: 2000000
	};
	url=i.url;
	download(url, options, function(err){
	    if (err) console.log("Got Error",err.message);
	    else console.log("meow");
	})
	// sleep(10);
})}