

var casper = require('casper').create();
var links;
casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X)');
function getLinks() {
// Scrape the links from top-right nav of the website
    var links = document.querySelectorAll('a');
    return Array.prototype.map.call(links, function (e) {
        return e.getAttribute('href')
    });
}

// Opens casperjs homepage
casper.start('https://m.dianping.com/shop/83462170/review_all');

// listener function for requested resources
var listener = function(requestData, request) {
    if (requestData.method === 'post'){
       
       this.echo(requestData.method);
       this.echo(requestData.postData);
    }else{
       this.echo(requestData.postData);
         }
};

// listening to all resources requests
casper.on("resource.requested", listener);


casper.on('resource.received', function(responseData) {
       this.echo(responseData.url);
       this.echo(responseData.status);  // slimerjs only
});
/*
casper.then(function () {
    links = this.evaluate(getLinks);
});


var url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_498321773?csrf_token='
casper.start(url, function() {
    var js = this.evaluate(function() {
        return document; 
    });    
    this.echo(js.all[0].outerHTML); 
});


casper.run(function () {
    for(var i in links) {
        console.log(links[i]);
    }
    casper.done();
});
*/

casper.run()
