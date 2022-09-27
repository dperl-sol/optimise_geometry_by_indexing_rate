#!/usr/bin/env cctbx.python

import json
import argparse
import copy
import dials.array_family.flex as flex

def get_args():
    parser = argparse.ArgumentParser(description='Strip duplicate reflections from ')
    parser.add_argument('working_directory', help='Directory to work in.')
    parser.add_argument('reference_name', help='DIALS .expt file to load.')
    parser.add_argument('input_expt', help='DIALS .expt file to load and strip duplicates from.')
    parser.add_argument('input_refl', help='DIALS .refl file to load and strip duplicates from.')
    parser.add_argument('output_name', help='new DIALS .expt and refl files to write (withpout extension)')
    return parser.parse_args()

def main():
    args = get_args()
    with open(args.working_directory+args.reference_name) as f:
        reference_expt = json.load(f)
    with open(args.working_directory+args.input_expt) as f:
        referent_expt = json.load(f)

    logging.info("Counting and indexing images in reference and referent expt files.")
    images_in_reference = [(ind, x['single_file_indices'][0]) for ind, x in enumerate(reference_expt['imageset'])]
    images_in_referent = [(ind, x['single_file_indices'][0]) for ind, x in enumerate(referent_expt['imageset'])]
    
    unique_image_indices = [x[0] for x in images_in_referent if not x[1] in [r[1] for r in images_in_reference]]

    logging.info("Counting and indexing images in reference and referent expt files")
    new_expt = copy.deepcopy(referent_expt)
    new_expt['experiment'] = [new_expt['experiment'][i] for i in unique_image_indices]
    new_expt['imageset'] = [new_expt['imageset'][i] for i in unique_image_indices]
    new_expt['beam'] = [new_expt['beam'][i] for i in unique_image_indices]
    new_expt['detector'] = [new_expt['detector'][i] for i in unique_image_indices]
    new_expt['crystal'] = [new_expt['crystal'][i] for i in unique_image_indices]

    old_id_new_index = {}
    for i, ex in enumerate(new_expt['experiment']):
        old_id_new_index[ex['beam']] = i
        ex['beam'] = i
        ex['detector'] = i
        ex['crystal'] = i
        ex['imageset'] = i
        
    logging.info(new_expt['experiment'])
    logging.info(old_id_new_index)
    
    with open(args.working_directory+args.output_name+'.expt', 'w') as f:
        json.dump(new_expt, f, indent=2)

    reflection_data = flex.reflection_table.from_file(args.working_directory+args.input_refl)

    unique_reflections = flex.bool([h in unique_image_indices for h in list(reflection_data["id"])])
    reflection_data = reflection_data.select(unique_reflections)

    logging.info(list(reflection_data["id"]))
    new_indices = flex.int([old_id_new_index[i] for i in list(reflection_data["id"])])
    reflection_data["id"] = new_indices
    
    reflection_data.as_msgpack_file(args.working_directory+args.output_name+'.refl')
    logging.info(list(reflection_data["id"]))



if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='log.txt',level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()