from DeltaFetcher import DeltaFetcher
dp = DeltaFetcher("https://github.com/joshio1/SimpleDb.git");

### Setup Repository Test ###
# result = dp.setup_repository();
# print result;
#
# with open("./vc/Readme.md") as f:
#     content = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# print content
#
# # print methods;
## Setup Repository Test End

### Get Changed Methods Test
methods = dp.get_changed_methods_for_current_build("5cc8e17d2bd48c651aed40b916365abe4e489796", "6f947501ef1acf0a998ccf55392239da2837c86f");
## Get Changed Methods Test End
