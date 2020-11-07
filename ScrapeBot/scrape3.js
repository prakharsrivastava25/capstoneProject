const puppeteer = require('puppeteer');
const fs = require('fs');

const save = async (value,i) => {
    // var jsonObj = value;
    var jsonContent = JSON.stringify(value);
    // var jsonContent = jsonObj;
    saveLoc=".\\urls\\url"+i+".json"
    fs.writeFile(saveLoc, jsonContent, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
        return console.log(err);
    }
    console.log("JSON file has been saved.");});
}

const scrapePage =async (page) => page.evaluate(() => {
    let data = []; // Create an empty array that will store our data
    let title = []; //Empty array for title
    let url = []; //Empty array for url
    let elements = document.querySelectorAll('.title-content');
    for (var element of elements){ 
        title.push(element.innerText);
    }
    console.log("HEre")
    elements = document.querySelectorAll('.csv'); 
    for (var element of elements){
        url.push(element.href);
    }

    for(i=0;i<url.length;i++){
        data.push({title:title[i],url:url[i]});
    }

    return data;
})


let scrape = async () => {
    let iterator=0;
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();

    await page.goto('https://data.gov.in/node/4643341');
    const result = [],iterResult=[];
    for( i=0; i<1200; i++){

        tempResult = await scrapePage(page)
        tempResult.forEach((datapoint) => {result.push(datapoint);iterResult.push(datapoint);});
    	console.log("waiting..");

        try{
        await page.click("#catalog-details-wrapper > div.content-wrapper > div > div.item-list > ul > li.pager-next > a");
    	} catch(err) {console.log(err, "\n Got error for i=",i,"\n");}
        await page.waitFor(8000);

        console.log("Done..")
        if(i%15==0) {
            save(iterResult,iterator.toString());
            iterator++;
            iterResult.length=0;
            // iterResult.splice(0,iterResult.length)
    }}
    browser.close();
    return result; // Return the data
};

scrape().then((value) => {
    save(value,"000");
});