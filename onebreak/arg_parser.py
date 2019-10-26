#! /usr/bin/env python

from .run import *
import argparse
from .version import __version__

def create_parser():

    parser = argparse.ArgumentParser(prog = "onebreak")

    parser.add_argument("--version", action = "version", version = "%(prog)s " + __version__)

    subparsers = parser.add_subparsers()


    ####################
    # parse
    parse = subparsers.add_parser("parse", 
                                  help = "Parse and cluster supporting read pairs for candidate breakpoints",
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
 
    parse.add_argument("bam_file", metavar = "input.bam", type = str,
                       help = "path to input bam file")

    parse.add_argument("output_file", metavar = "output_file", type = str,
                       help = "path to output file")

    parse.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    parse.add_argument("--key_seq_size", type = int, default = 8,
                       help = "size of junction bases on breakpoint to classify the breakpoint (default: %(default)s)")

    parse.add_argument("--min_major_clip_size", type = int, default = 8,
                       help = "minimum number of clipped bases for junction read (default: %(default)s)")

    parse.add_argument("--max_minor_clip_size", type = int, default = 15,
                       help = "if the clipped bases numbers of both sides are greater than this value, then the read is filtered out (default: %(default)s)")

    parse.add_argument("--check_interval", type = int, default = 1000000,
                       help = "the default value will work for most cases. but when memory flows, please try reducing this value (default: %(default)s)")

    parse.set_defaults(func = parse_main)
    ####################   

    # merge control
    merge_control = subparsers.add_parser("merge_control",
                                          help = "merge, compress and index break point file generated by parse function",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    merge_control.add_argument("bp_file_list", metavar = "bp_file_list.txt", default = None, type = str,
                               help = "breakpoint ifle path list")

    merge_control.add_argument("output_file", default = None, type = str,
                               help = "the path of the output file")

    merge_control.add_argument("--support_num_thres", type = int, default = 2,
                               help = "remove breakpoints whose supporting numbers are below this value (default: %(default)s)")

    merge_control.add_argument("--sample_num_thres", type = int, default = 2,
                               help = "register breakpoints at least shared by specified number of samples (default: %(default)s)")

    merge_control.set_defaults(func = merge_control_main)


    ####################
    filt = subparsers.add_parser("filt", 
                                 help = "Filter candidate somatic breakpoint")

    filt.add_argument("tumor_bp_file", metavar = "tumor_bp_file.txt.gz", type = str,
                      help = "path to tumor breakpoint file generated by parse function")

    filt.add_argument("tumor_bam", metavar = "tumor.bam", type = str,
                      help = "path to tumor bam file")

    filt.add_argument("output_file", metavar = "output.txt", type = str,
                      help = "path to output file")

    filt.add_argument("reference_genome", metavar = "reference.fa", type = str,
                      help = "path to reference genome")

    filt.add_argument("--matched_control_bp_file", metavar = "matched_control_bp_file.txt.gz", default = "", type = str,
                      help = "path to matched control breakpoint file generated by parse function")

    filt.add_argument("--matched_control_bam", metavar = "matched_control.bam", default = "", type = str,
                             help = "path to matched control bam file")

    filt.add_argument("--merged_control_file", metavar = "merged_control.txt.gz", default = "", type = str,
                             help = "path to the non-matched control panel data generated by merge function")

    # filt_parser.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    filt.add_argument("--min_second_juncseq_baseq", type = int, default = 30,
                      help = "threshould of the second juncseq base quality")

    filt.add_argument("--min_variant_num_tumor", type = int, default = 3,
                      help = "minimum required number of supporting read (default: %(default)s)")

    filt.add_argument("--min_VAF_tumor", type = float, default = 0.07,
                      help = "minimum required allele frequency of the tumor sample (default: %(default)s)")

    filt.add_argument("--max_variant_num_control", type = int, default = 1,
                      help = "maximum allowed number of reads in matched control sample (default: %(default)s)")

    filt.add_argument("--max_VAF_control", type = float, default = 0.02,
                      help = "maximum allowed allele frequency of matched control sample (default: %(default)s)")

    filt.add_argument("--max_fisher_pvalue", type = float, default = 0.10,
                      help = "maximum allowed fisher's exact test p-value (default: %(default)s)")

    filt.add_argument("--min_median_mapq", type = int, default = 40,
                      help = "threshold of mapping quality (if the median of supporting reads is below this value, then filtered out) (default: %(default)s)")

    filt.add_argument("--min_max_clip_size", type = int, default = 30,
                      help = "threshould of maximum clipped size (if the maximum clipped size is below this value, then filtered out) (default: %(default)s)")

    filt.add_argument("--min_unique_clip_sizes", type = int, default = 2,
                      help = "threshould of unique clipped sizes (default: %(default)s)")

    filt.add_argument("--ignore_juncseq_consistency", action='store_true', default=False, 
                             help = "ignore juncseq consistency when comparing with control")

    filt.add_argument("--permissible_range", type = int, default = 0,
                      help = "permissible range for control breakpoint search")

    filt.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    filt.set_defaults(func = filt_main)
    ####################
    # contig
    contig = subparsers.add_parser("contig",
                                   help = "Generate contig by assembling supprint reads candidate somatic breakpoint")

    contig.add_argument("tumor_bp_filt_file", metavar = "tumor_bp_filt.txt", type = str,
                         help = "path to tumor filetered breakpoint file generated by filt function")

    # contig.add_argument("tumor_bp_file", metavar = "tumor_bp_file.txt.gz", type = str,
    #                      help = "path to tumor breakpoint file generated by parse function")

    contig.add_argument("tumor_bam", metavar = "tumor.bam", type = str,
                        help = "path to tumor bam file")

    contig.add_argument("output_file", metavar = "output.txt", type = str,
                        help = "path to output file")

    contig.add_argument("reference_genome", metavar = "reference.fa", type = str,
                        help = "path to reference genome")

    contig.add_argument("--fermi_lite_option", type = str, default = "-l 20",
                        help = "option for fermi-lite")

    """
    contig.add_argument("--blat_option", type = str, default = "-stepSize=5 -repMatch=2253",
                        help = "option used in blat")

    contig.add_argument("--blat_ooc", type = str, default = "",
                        help = "path to ooc file")
 
    contig.add_argument("--virus_db", type = str, default = "",
                        help = "path to virus sequence database (fasta format)")

    contig.add_argument("--repeat_db", type = str, default = "",
                        help = "path to repeat sequence database (fasta format)")

    contig.add_argument("--mitochondria_db", type = str, default = "",
                        help = "path to mitochondria sequence database (fasta format)")

    contig.add_argument("--adapter_db", type = str, default = "",
                        help = "path to bacteria sequence database (fasta format)")
    """

    contig.add_argument("--min_contig_length", type = int, default = 0,
                      help = "threshould of minimum contig length (if the generated contig size is below this value, then filtered out) (default: %(default)s)")

    # contig.add_argument("--swalign_length", type = int, default = 20,
    #                   help = "threshould of minimum Waterman-Smith alignment length (if the generated contig size is below this value, then filtered out) (default: %(default)s)")

    # contig.add_argument("--swalign_score", type = int, default = 35,
    #               help = "threshould of minimum Waterman-Smith alignment score (default: %(default)s)")

    contig.set_defaults(func = contig_main)

    ####################
    # long_read_validate
    long_read_validate = subparsers.add_parser("long_read_validate",
                                               help = "validate break points using long read sequence data")

    long_read_validate.add_argument("contig_result_file", metavar = "contig_result_file", type = str,
                                    help = "path to contig function result file")

    long_read_validate.add_argument("output_file", metavar = "output_file", type = str,
                                    help = "path to output file")
 
    long_read_validate.add_argument("tumor_bam", metavar = "tumor.bam", type = str,
                                    help = "path to tumor bam file")

    long_read_validate.add_argument("reference_genome", metavar = "reference.fa", type = str,
                                    help = "path to reference genome")

    long_read_validate.add_argument("--control_bam", metavar = "control.bam", type = str, default = None,
                                    help = "path to control bam file")

    long_read_validate.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    long_read_validate.set_defaults(func = long_read_validate_main)

    ####################
    #classify
    classify = subparsers.add_parser("classify",
                               help = "classify SVs into canonical and non-canonical SVs")

    classify.add_argument("contig_result_file", metavar = "contig_result_file", type = str,
                          help = "path to contig function result file")

    classify.add_argument("output_file", metavar = "output_file", type = str,
                          help = "path to output file")

    classify.add_argument("reference_genome", metavar = "reference.fa", type = str,
                          help = "path to human reference genome")

    classify.add_argument("--te_seq", metavar = "te_seq.fa", type = str, default = None,
                          help = "path to transposable elements sequence file")

    classify.add_argument("--simple_repeat", metavar = "simple_repeat.bed.gz", type = str, default = None,
                          help = "path to tabix indexed simple repeat bed.gz file")

    classify.add_argument("--remove_rna", default = False, action = "store_true",
                          help = "remove putative rna splicing junction contamination (default: %(default)s)")

    classify.set_defaults(func = classify_main)
    ###

    return parser

