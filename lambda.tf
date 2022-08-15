resource "aws_lambda_function" "ec2lambda" {
    filename = "describe_ec2_lambda.zip"
    function_name = "list"
    role = aws_iam_role.lambda_role.arn
    runtime = "python3.9"
    handler = "list.lambda_handler"
    source_code_hash = filebase64sha256("describe_ec2_lambda.zip")
}