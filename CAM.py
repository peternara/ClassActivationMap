import matplotlib.pyplot as plt
import tensorflow as tf
import os
from skimage.io import imsave

def get_class_map(name,x , label , im_width):
    out_ch = int(x.get_shape()[-1])
    conv_resize=tf.image.resize_bilinear(x,[im_width , im_width])
    with tf.variable_scope(name , reuse = True) as scope:
        label_w = tf.gather(tf.transpose(tf.get_variable('w')) , label)
        label_w = tf.reshape(label_w , [-1, out_ch , 1])
    conv_resize = tf.reshape(conv_resize , [-1 , im_width *im_width , out_ch])
    classmap = tf.matmul(conv_resize , label_w)
    classmap = tf.reshape(classmap ,[-1 , im_width , im_width])
    return classmap


def inspect_cam(sess, cam , top_conv ,test_imgs, test_labs, global_step , num_images , x, y_ , y):
    try:
        os.mkdir('./out');
    except Exception:
        pass;

    for s in range(num_images):
        save_dir='./out/img_{}'.format(s)
        try:os.mkdir(save_dir);
        except Exception:pass;
        if __debug__ ==True:
            print test_imgs[s].shape
        if test_imgs[s].shape[-1]==1:
            imsave('{}/image_test.png'.format(save_dir) ,test_imgs[s].reshape([test_imgs[s].shape[0] , test_imgs.shape[1]]))
        else :
            imsave('{}/image_test.png'.format(save_dir), test_imgs[s])
        img = test_imgs[s:s+1]
        label = test_labs[s:s+1]
        conv_val , output_val =sess.run([top_conv , y] , feed_dict={x:img})
        cam_ans= sess.run( cam ,  feed_dict={ y_:label , top_conv:conv_val })
        cam_vis=list(map(lambda x: (x-x.min())/(x.max()-x.min()) , cam_ans))
        for vis , ori in zip(cam_vis , img):

            if ori.shape[-1]==1: #grey
                plt.imshow( 1-ori.reshape([ori.shape[0] , ori.shape[1]]))
            plt.imshow( vis.reshape([vis.shape[0] , vis.shape[1]]) , cmap=plt.cm.jet , alpha=0.5 , interpolation='nearest' , vmin=0 , vmax=1)
            cmap_file='{}/cmap_{}.png'.format(save_dir, global_step)
            plt.savefig(cmap_file)
            plt.close();