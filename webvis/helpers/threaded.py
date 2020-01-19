import multiprocessing.dummy as thr

def threaded(f,*args, **kwargs):
    p = thr.Process(target=(f),args = args, **kwargs)
    p.start()
    return p
