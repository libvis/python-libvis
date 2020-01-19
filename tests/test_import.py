import time

def test_import():
    t = time.time()
    import libvis
    dt = time.time() - t
    print("Import time:", dt)

