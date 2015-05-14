__author__ = 'sdouglas'


from XCCDF_Parser import Parse as xccdf_parser


def main():
    xccdf = xccdf_parser("sample_files/redhat-stig/U_RedHat_6_V1R7_STIG_SCAP_1-1_Benchmark-xccdf.xml")
    stig_list = xccdf.construct_dictionary()
    for i in stig_list:
        xccdf.pretty_print_dict(i)


if __name__ == "__main__":
    main()
