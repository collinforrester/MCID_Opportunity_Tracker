# Multi-customer Immersion Day Idea Tracker



## Customization instructions
You will want to modify the source code for your event and your environment.
  1. Modify '.ebextensions/options.config' file:
     * Row 3: Update your email to be notified via SNS when new items are added to the table.
     * Row 6: Update the SESSION value to identify the event name.
  2. Lorem Ipsum


## Deploy the application

You can deploy the application using the following steps:
  1. [Install the AWS Elastic Beanstalk Command Line Interface (CLI)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html).
  2. Create an IAM Instance Profile named **aws-elasticbeanstalk-sample-role** with the policy in [iam_policy.json](iam_policy.json). For more information on how to create an IAM Instance Profile, see [Create an IAM Instance Profile for Your Amazon EC2 Instances](https://docs.aws.amazon.com/codedeploy/latest/userguide/how-to-create-iam-instance-profile.html).
  3. Run `eb init -r <region> -p "Node.js"` to initialize the folder for use with the CLI. Replace `<region>` with a region identifier such as `us-west-2` (see [Regions and Endpoints](https://docs.amazonaws.cn/en_us/general/latest/gr/rande.html#elasticbeanstalk_region) for a full list of region identifiers). 
  4. Run `eb create --instance_profile aws-elasticbeanstalk-sample-role` to begin the creation of your environment.
     * Enter the environment name of your choice.
     * Enter the CNAME prefix you want to use for this environment.
  5. After modifications to the source code, run `eb deploy` to update the environment.
  6. Once the environment creation process completes, run `eb open` to open the application in a browser.
  7. Run `eb terminate --all` to clean up.


## This tool was based on the [AWS Elastic Beanstalk Express Sample App](https://github.com/aws-samples/eb-node-express-sample)
This sample application uses the [Express](https://expressjs.com/) framework and [Bootstrap](http://getbootstrap.com/) to build a simple, scalable customer signup form that is deployed to [AWS Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/). The application stores data in [Amazon DynamoDB](http://aws.amazon.com/dynamodb/) and publishes notifications to the [Amazon Simple Notification Service (SNS)](http://aws.amazon.com/sns/) when a customer fills out the form.
