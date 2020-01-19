import time

def test_import():
    t = time.time()
    import webvis
    dt = time.time() - t
    print("Import time:", dt)

