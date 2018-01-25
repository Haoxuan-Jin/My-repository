export token=$your_token
export bill=$your_bill
target_id=file_id.txt
source=file_source.txt
new_id=file_new_id.txt
project=haoxuan-modify-metadata3
user=jinhaoxuan
tmp=tmp_file.txt

#get your billing id
curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/billing/groups"|jq

#create a new project
curl --data '{"name": "'$project'", "description": "A project for testing modify file metadata", "billing_group": "'$bill'"}' -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X POST "https://cavatica-api.sbgenomics.com/v2/projects"|jq

#list all files from source project
line=100
limit=100
offset=1
check=1
until [ $line -le $check ]
do
curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files?limit=$limit&offset=$offset&project=yuankun/bgi-practise-source"|python -m json.tool > $tmp
line=`grep 'id' $tmp|wc -l`
offset=`expr $offset + 100`
cat $tmp >> $source
done

#list all files from target project

line=100
offset=1
until [ $line -le $check ]
do
curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files?limit=$limit&offset=$offset&project=yuankun/bgi-practise-target"|python -m json.tool | grep 'id' | sed  's;            "id": ;;'|sed 's;,;;'|sed 's;";;g' > $tmp
line=`cat $tmp|wc -l`
offset=`expr $offset + 100`
cat $tmp >> $target_id
done


#copy file to new project
for i in `cat $target_id`;
do
curl --data '{"project": "'$user'/'$project'", "file_ids": ["'$i'"]}' -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X POST "https://cavatica-api.sbgenomics.com/v2/action/files/copy"|jq;
done

#get new files id from new project
curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files?limit=500&project=$user/$project"|python -m json.tool | grep 'id' | sed  's;            "id": ;;'|sed 's;,;;'|sed 's;";;g' > $new_id
line=100
offset=1
until [ $line -le $check ]
do
curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files?limit=$limit&offset=$offset&project=$user/$project"|python -m json.tool | grep 'id' | sed  's;            "id": ;;'|sed 's;,;;'|sed 's;";;g' > $tmp
line=`cat $tmp|wc -l`
offset=`expr $offset + 100`
cat $tmp >> $new_id
done

#get metadata from source project
for i in `cat $new_id` ;
do
name=`curl -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files/$i"|python -m json.tool |grep 'name' |sed 's;"name": ;;'|sed 's;,;;'|sed 's;";;g' `
source_id=`grep -B 1 $name $source|grep 'id'|sed  's;            "id": ;;'|sed 's;,;;'|sed 's;";;g'`
metadata=`curl  -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X GET "https://cavatica-api.sbgenomics.com/v2/files/$source_id/metadata"|sed 's;:;: ;g'`

#modify metadata
curl --data "$metadata" -s -H "X-SBG-Auth-Token: $token" -H "content-type: application/json" -X PATCH "https://cavatica-api.sbgenomics.com/v2/files/$i/metadata" |jq
done

#


