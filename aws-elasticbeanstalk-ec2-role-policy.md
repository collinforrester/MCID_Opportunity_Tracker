## aws-elasticbeanstalk-ec2-role IAM policy
An IAM role must be created for the EC2 instance to be able to write to DynamoDB and publish to the SNS topic.

[Create an IAM EC2 service role](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-iam-instance-profile.html) with the following inline policy.  

If manually deploying the application, this role is attached to the "IAM instance profile" virtual machine permissions section of the EB security configuration area of the Elastic Beanstalk web console.

<pre><code>
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "dynamodb:PutItem"
              ],
              "Resource": [
                  "*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "sns:Publish"
              ],
              "Resource": [
                  "*"
              ]
          }
      ]
  }
</code></pre>
