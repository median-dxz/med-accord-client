for file in ./accord_client/ui/*.ui
do
  export OUTPUT_FILE="./accord_client/ui/$(echo ${file} | sed "s/.*\///" | sed "s/.ui/.py/" | sed "s/^/ui_/")"
  echo "Generating ${file} -> ${OUTPUT_FILE}"
  pyuic6 -o $OUTPUT_FILE -x $file
done