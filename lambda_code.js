'use strict';
var AWS = require("aws-sdk");
var sns = new AWS.SNS();

exports.handler = (event, context, callback) => {

    event.Records.forEach((record) => {
        console.log('Stream record: ', JSON.stringify(record, null, 2));

        if (record.eventName == 'INSERT') {
            var who = JSON.stringify(record.dynamodb.NewImage.latitude.S).slice(2,9);
            var when = JSON.stringify(record.dynamodb.NewImage.longitude.S).slice(1,9);
            // var message = JSON.stringify(record.dynamodb.NewImage.message.S).slice(1,9);
           
            
            
            // var what = JSON.stringify(record.dynamodb.NewImage.Message.S);
            var params = {
                Subject: 'Your vehicle is Crashed!!',
                Message: "Unfortunately, Your registered Vehicle has been crashed.\n Your Vehicle Number is : GJ-XXXX-XX.\n\n  We hope the following information will be helpful for you.\n Location : http://maps.google.com/?q=" + who + ',' + when + "\n\n",
                TopicArn: 'arn:aws:sns:us-east-1:021251467591:Alert_Vehicle'
            };
            sns.publish(params, function(err, data) {
                if (err) {
                    console.error("Unable to send message. Error JSON:", JSON.stringify(err, null, 2));
                } else {
                    console.log("Results from sending message: ", JSON.stringify(data, null, 2));
                }
            });
        }
    });
    callback(null, `Successfully processed ${event.Records.length} records.`);
};   