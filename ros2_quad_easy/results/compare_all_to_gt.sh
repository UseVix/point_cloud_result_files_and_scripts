find . -name "*tum.txt" | while read -r file; do
    output=$( echo $file | head -c -5 )  # Remove suffix
    output="/media/risalinux/Seagate Basic/Dataset/NewerCollege/quad_easy/bag/comparison_with_gt_results/$(echo ${output} | awk -F'/' '{print $NF}')"
    echo "Plik zapisu"
    echo $output
    echo "Plik odczytywany"
    echo $file
    evo_ape tum ../../../gt/gt-nc-quad-easy.tum "$file" --align --save_results "$output"
done

