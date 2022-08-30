resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "python.zip"
  layer_name = "lambda_layer_python"
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "ec2lambda" {
    filename = "describe_ec2_lambda.zip"
    function_name = "list"
    role = aws_iam_role.lambda_role.arn
    runtime = "python3.9"
    handler = "list.lambda_handler"
    source_code_hash = filebase64sha256("describe_ec2_lambda.zip")
}