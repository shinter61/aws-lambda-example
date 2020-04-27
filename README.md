## aws-lambda-sample

serverless + lambda + codepipeline + codebuild によるサーバーレスアプリケーション

メールアドレスの存在検証を行う

1リクエストにつき200件までのメールアドレス検証が可能

### Usage

```rb
conn = Faraday::Connection.new(:url => 'https://lambda-api-endpoint') do |builder|
  builder.request :url_encoded
  builder.response :logger
  builder.adapter  :net_http
end

mail_address_arr = (1..200).map { |i| "test#{i}@qmail.com" }

response = conn.post do |req|
  req.url '/dev'
  req.body = {
    mailAddresses: mail_address_arr
  }
end
```

### Reference

https://qiita.com/cm_sato_naoya/items/6a99acac9b833a5fae8e
https://qiita.com/horike37/items/b295a91908fcfd4033a2
https://dev.classmethod.jp/articles/easy-deploy-of-lambda-with-serverless-framework/
https://qiita.com/Esfahan/items/736d09f732fa619d2410
https://qiita.com/miya0001/items/73c9be558b7033eab2c1
https://qiita.com/yokoyan/items/7a39a99996f2ade4af5b
https://sysadmins.co.za/parallel-processing-on-aws-lambda-with-python-using-multiprocessing/
https://qiita.com/simonritchie/items/1ce3914eb5444d2157ac
