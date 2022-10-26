#!/usr/bin/env bash

has_changes="false"
# Create empty stack in review in progress stage w/ change set or create change set for existing stack
# shellcheck disable=SC2086
aws cloudformation deploy --stack-name "$INPUT_STACK_NAME" --template-file $INPUT_TEMPLATE_FILE  --no-fail-on-empty-changeset --no-execute-changeset $INPUT_OPTIONS

change_set_name=$(aws cloudformation list-change-sets --stack-name "$INPUT_STACK_NAME" | jq .Summaries[0].ChangeSetName | tr -d '"')
# If change_set_name is not null, describe and put output to a json file. Delete the change set and process the json
# to make the html report.
if [ "$change_set_name" != "null" ]; then
  aws cloudformation describe-change-set --stack-name "$INPUT_STACK_NAME" --change-set-name "$change_set_name" --output json > "$INPUT_STACK_NAME".json
  aws cloudformation delete-change-set --stack-name "$INPUT_STACK_NAME" --change-set-name="$change_set_name"
  results=$(python /format_json_to_html.py "$INPUT_STACK_NAME" "$INPUT_STACK_NAME".json "$INPUT_ENVIRONMENT")
  
  # shellcheck disable=SC2002
  numberOfChanges=$(cat "$INPUT_STACK_NAME".json | jq .Changes | jq length)
  if [ "$numberOfChanges" != "0" ]; then
    has_changes="true"
  fi

  echo "results=$results" >> $GITHUB_OUTPUT
  ## cleanup of empty stack if no resources and status is in review in progress, enables create change set to work
  numOfResources=$(aws cloudformation list-stack-resources --stack-name "$INPUT_STACK_NAME" --output json | jq .StackResourceSummaries | jq length)
  status=$(aws cloudformation describe-stacks --stack-name "$INPUT_STACK_NAME" --output json | jq .Stacks[0].StackStatus | tr -d '"')
  if [ "$status" == "REVIEW_IN_PROGRESS" ] && [ "$numOfResources" == "0" ]; then
    aws cloudformation delete-stack --stack-name "$INPUT_STACK_NAME"
  fi
fi

echo "has-changes=$has_changes" >> $GITHUB_OUTPUT
