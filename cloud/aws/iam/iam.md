## Roles

### Service Roles

A service role is an IAM role that you create so that an AWS service can do work in your account on your behalf.

- Who can use the role → the trust policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
- What the role can do → the permissions policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadReports",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-reports-bucket/*"
    },
    {
      "Sid": "WriteLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

### Service Linked Roles

A service-linked role is a role that an AWS service owns and uses to manage resources in your account on your behalf. AWS defines it completely.

You don’t write its trust policy or its permissions, and you generally can’t change them.

- Names will start with `AWSServiceRoleFor...` 
- Examples:
  - `AWSServiceRoleForElasticLoadBalancing`
  - `AWSServiceRoleForECS`
  - `AWSServiceRoleForRDS`

Creation of these roles are usually automatic, the first time you use a feature that needs one. The person triggering it needs `iam:CreateServiceLinkedRole`

**Use case: Running an ECS service in ECS Fargate Cluster**

- `AWSServiceRoleForApplicationAutoScaling_ECSService`
- `AWSServiceRoleForECS`
- `Task execution role`
- `Task role`

`AWSServiceRoleForECS` is the role ECS uses to manage the AWS resources around your tasks: networking, load balancers, service discovery, and so on.

It never touches what your application code does, that’s the job of the task role. Only `ecs.amazonaws.com` is trusted to assume it, and its permissions come from the AWS-managed policy `AmazonECSServiceRolePolicy`.

```bash
→ aws iam list-roles --path-prefix /aws-service-role/ --query "Roles[?contains(RoleName, 'ECS')].RoleName" --output table
---------------------------------------------------------------------------------------------------------------------------------------------
|                       ListRoles                      |                       Policy                                                       |
+------------------------------------------------------|------------------------------------------------------------------------------------|
|  AWSServiceRoleForApplicationAutoScaling_ECSService  | arn:aws:iam::aws:policy/aws-service-role/AWSApplicationAutoscalingECSServicePolicy |
|  AWSServiceRoleForECS                                | arn:aws:iam::aws:policy/aws-service-role/AWSECSServicePolicy                       |
+------------------------------------------------------|------------------------------------------------------------------------------------+
```

### Pass Role

`iam:PassRole` is the permission that lets you hand a service role to an AWS service. 

**Use case: a developer creating a Lambda function**

Let's say a developer wants to create a Lambda function that reads files from an S3 bucket.

- An admin has already created a service role called `lambda-s3-reader-role` with the permission `s3:GetObject` on a bucket and it trusts `lambda.amazonaws.com`
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
