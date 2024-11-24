resource "aws_lambda_function" "lambda" {
  function_name    = var.lambda_name
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  layers           = [aws_lambda_layer_version.requirements_lambda_layer.arn]
  role             = aws_iam_role.lambda_role.arn
  timeout          = 29

  environment {
    variables = {
      "ENV" = "dev",
      "GEMINI_API_KEY" = var.gemini_api_key,
      "TZ" = "America/Sao_Paulo"
    }
  }
}

data "archive_file" "code" {
  type        = "zip"
  source_dir  = "${local.source_code_path}"
  excludes    = ["venv"]
  output_path = "${path.module}/code.zip"
}