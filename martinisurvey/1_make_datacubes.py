from sample import targets
from multiprocessing import Pool

views = [view for target in targets for view in target.views]


def makecube(view):
    print(view)
    view.generate_datacube()
    return


pool = Pool(20)
pool.map(makecube, views, chunksize=1)
