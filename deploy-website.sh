curl --location --request GET "http://dreamtobe.cn:9006/hooks/deploy-website" \
  --header "D-check: ${DEPLOY_CHECK_KEY}" \
  --header "required: blog"
