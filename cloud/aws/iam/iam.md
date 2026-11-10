### Roles

#### Service Roles

#### Service Linked Roles

#### Pass Role

`iam:PassRole` is the permission that lets you hand a service role to an AWS service. 

**Use case: a developer creating a Lambda function**

Let's say a developer wants to create a Lambda function that reads files from an S3 bucket.

- An admin has already created a service role called `lambda-s3-reader-role` withbthe permission `s3:GetObject` on a bucket and it trusts `lambda.amazonaws.com`
- The developer calls `lambda:CreateFunction` and specifies `lambda-s3-reader-role` as the execution role.
- Before AWS accepts this, it checks two things:
    - Does the developer have `lambda:CreateFunction`?
    - Does the developer `iam:PassRole` on `lambda-s3-reader-role`?
- If both checks pass, the function is created. Lambda then assumes the role whenever the function runs.
- Below is an example policy attached to the developer.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:CreateFunction",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/lambda-s3-reader-role",
      "Condition": {
        "StringEquals": { "iam:PassedToService": "lambda.amazonaws.com" }
      }
    }
  ]
}
```

