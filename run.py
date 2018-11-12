from app import app
import multiprocessing as mp

if __name__=='__main__':
    mp.set_start_method('forkserver', force=True)
    app.run(host="localhost", port=5000, debug=True)
