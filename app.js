// Include the cluster module
var cluster = require('cluster');

// Include uuid
//const uuidv4 = require('uuid/v4');

// Code to run if we're in the master process
if (cluster.isMaster) {

    // Count the machine's CPUs
    var cpuCount = require('os').cpus().length;

    // Create a worker for each CPU
    for (var i = 0; i < cpuCount; i += 1) {
        cluster.fork();
    }

    // Listen for terminating workers
    cluster.on('exit', function (worker) {

        // Replace the terminated workers
        console.log('Worker ' + worker.id + ' died :(');
        cluster.fork();

    });

// Code to run if we're in a worker process
} else {
    var AWS = require('aws-sdk');
    var express = require('express');
    var bodyParser = require('body-parser');

    AWS.config.region = process.env.REGION

    var sns = new AWS.SNS();
    var ddb = new AWS.DynamoDB();

    var ddbTable =  process.env.IDEAS_TABLE;
    var snsTopic =  process.env.IDEAS_TOPIC;
    var app = express();

    app.set('view engine', 'ejs');
    app.set('views', __dirname + '/views');
    app.use(bodyParser.urlencoded({extended:false}));

    app.get('/', function(req, res) {
        res.render('index', {
            static_path: 'static',
            theme: process.env.THEME || 'amelia',
            session: process.env.SESSION || 'NoSessionID',
            flask_debug: process.env.FLASK_DEBUG || 'false'
        });
    });

    // app.post('/idea', function(req, res) {
    //     var dt = new Date();
    //     var utcDate = dt.toUTCString();
    //     var uuid = uuidv4.v4();
    //     var item = {
    //         'Email': {'S': req.body.email},
    //         'Name': {'S': req.body.name},
    //         'Company': {'S': req.body.company},
    //         'Idea': {'S': req.body.idea},
    //         'SessionID': {'S': process.env.SESSION},
    //         'UUID': {'S': uuid},
    //         'DateTime': {'S': utcDate}
    //     };

    app.post('/idea', function(req, res) {
        var dt = new Date();
        var utcDate = dt.toUTCString();
        var item = {
            'Email': {'S': req.body.email},
            'Name': {'S': req.body.name},
            'Company': {'S': req.body.company},
            'Idea': {'S': req.body.idea},
            'SessionID': {'S': process.env.SESSION},
            'DateTime': {'S': utcDate}
        };

        ddb.putItem({
            'TableName': ddbTable,
            'Item': item,
            'Expected': { Email: { Exists: false } }
        }, function(err, data) {
            if (err) {
                var returnStatus = 500;

                if (err.code === 'ConditionalCheckFailedException') {
                    returnStatus = 409;
                }

                res.status(returnStatus).end();
                console.log('DDB Error: ' + err);
            } else {
                sns.publish({
                    'Message': 'Name: ' + req.body.name + "\r\nEmail: " + req.body.email
                                        + "\r\nSession: " + process.env.SESSION
                                        + "\r\nCompany: " + req.body.company,
                    'Subject': 'Idea Submitted!!!',
                    'TopicArn': snsTopic
                }, function(err, data) {
                    if (err) {
                        res.status(500).end();
                        console.log('SNS Error: ' + err);
                    } else {
                        res.status(201).end();
                    }
                });
            }
        });
    });

    var port = process.env.PORT || 3000;

    var server = app.listen(port, function () {
        console.log('Server running at http://127.0.0.1:' + port + '/');
    });
}
