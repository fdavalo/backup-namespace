kind=$1
ns=$2
name=$3
dir=$4

mkdir -p $dir/$ns/$kind
if [[ $ns == "none" ]]; then
	oc get --ignore-not-found $kind/$name -o json > $dir/$ns/$kind/$name.json
else
	oc get --ignore-not-found $kind/$name -n $ns -o json > $dir/$ns/$kind/$name.json
fi
if [[ -s $dir/$ns/$kind/$name.json ]]; then
	python3 backup-yaml.py $name $kind $dir/$ns/$kind/
fi
/bin/rm -f $dir/$ns/$kind/$name.json
if [[ ! -s $dir/$ns/$kind/$name.yaml ]]; then /bin/rm -f $dir/$ns/$kind/$name.yaml; fi
if [[ ! $(ls -A $dir/$ns/$kind) ]]; then /bin/rm -fd $dir/$ns/$kind; fi
