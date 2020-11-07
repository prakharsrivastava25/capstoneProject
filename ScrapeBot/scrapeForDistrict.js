const puppeteer = require('puppeteer');
const fs = require('fs');
var BreakException = {};

const save = async (value,state,district) => {
    // var jsonObj = value;
    var jsonContent = JSON.stringify(value);
    // var jsonContent = jsonObj;

    var dir = ".\\WholeUrls\\"+state;

    if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
    }

    saveLoc=".\\WholeUrls\\"+state+"\\"+district+".json"
    fs.writeFile(saveLoc, jsonContent, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
        return console.log(err);
    }
    console.log("JSON file has been saved.");});
}

const scrapePage =async (page) => page.evaluate(() => {
    let url = []; //Empty array for url
    let title = [];
    let elements = document.querySelectorAll('.csv'); 
    for (var element of elements){
        url.push(element.href);
    }

    elements = document.querySelectorAll('.title-content');
    for (var element of elements){ 
        title.push(element.innerText);
    }

    let data = {title,url};

    return data;
})

let scrape = async (district="BAKSA",state="ASSAM") => {
    console.log("scraping started for ", district)
    let iterator=0;
    d=district.toLowerCase()
    district=""

    for(const i in d){
        if(i!=' ') district+=d[i]; else break;
    }
    


    
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    //for all urls
    urls=[]
    uRl='https://data.gov.in/search/site?filter%5Bnew_title%5D=farmers%20queries%20kisan%20call%20centre%20'+district+'%20district%20month'
    await page.goto(uRl);
    i1=1;
    while (1){
        for (let i = 0; i < 10; ++i) {
            let Result;
            
            Result = `#ogpl-cust-result-html-wrap > div:nth-child(${i + 1}) > h3 > a`;
            
            try{
                await page.waitFor(Result, {visible: true});
            }    
            catch(err){
                console.log("Came Here")
                i1=0;
                break;
            }
            
        
            page.click(Result);
            await page.waitForNavigation();
            //const url = page.evaluate(()=> {uRL= document.querySelector('.csv');return uRL.href;})
            url= await scrapePage(page);
            urls.push(url);
            // save(urls,state,district)
            await page.goBack();
            // await page.waitForNavigation();
        }
        if(i1==0)
                break;
        

        let Result = `#ogpl-cust-result-pager-wrap > div > ul > li:nth-child(2) > a`;
        try{
            await page.waitFor(Result, {visible: true});
        }
        catch(err){
            Result = `#ogpl-cust-result-pager-wrap > div > ul > li > a`;
        }
        page.click(Result);
        await page.waitForNavigation();
    }

    browser.close();

    if(JSON.stringify(urls)!="[]")
        save(urls,state,district)

    return new Promise((resolve)=> resolve('resolved'));

};

module.exports =    {scrape};

// scrape().then((value,state,district) => {
//     save(value,state,district);
// });