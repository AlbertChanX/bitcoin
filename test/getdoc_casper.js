# http://techslides.com/grabbing-html-source-code-with-phantomjs-or-casperjs


var casper = require('casper').create();
var url = 'http://instagram.com/';

casper.start(url, function() {
    var js = this.evaluate(function() {
        return document; 
    });    
    this.echo(js.all[0].outerHTML); 
});
casper.run();

 
