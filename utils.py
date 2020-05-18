# coding:utf-8
# 使用BFM模型生成3DMM信息，并保存在.ply文件中
import numpy as np
import cv2

def projectBackBFM_withEP(model, features, expr_paras, pose_paras):
	# Shape
	alpha = model.shapeEV * 0
	for it in range(0, 99):
		alpha[it] = model.shapeEV[it] * features[it]
	S = np.matmul(model.shapePC, alpha)

	# Expression
	expr = model.expEV * 0
	for it in range(0, 29):
		expr[it] = model.expEV[it] * expr_paras[it]
	E = np.matmul(model.expPC, expr)

	## Adding back average shape and average expression
	S = model.shapeMU + S + model.expMU + E
	numVert = S.shape[0]/3

	# Pose
	r = pose_paras[0:3]
	r[1] = -r[1]
	r[2] = -r[2]
	t = pose_paras[3:6]
	t[0] = -t[0]
	R, jacobian = cv2.Rodrigues(r, None)

	S = np.reshape(S,(numVert,3))
	S_RT = np.matmul(R, np.transpose(S)) + np.reshape(t, [3,1])
	S_RT = np.transpose(S_RT)

	# (Texture)
	beta = model.texEV * 0
	for it in range(0, 99):
		beta[it] = model.texEV[it] * features[it+99]
	T = np.matmul(model.texPC, beta)
	## Adding back average texture
	T = model.texMU + T
	## Some filtering
	T = [truncateUint8(value) for value in T]
	## Final Saving for visualization
	S = np.reshape(S_RT,(numVert,3))
	T = np.reshape(T,(numVert, 3))

	return S,T

def truncateUint8(val):
	if val < 0:
		return 0
	elif val > 255:
		return 255
	else:
		return val


def write_ply_textureless(fname, S, faces):
	nV = S.shape[0]
	nF = faces.shape[0]
	f = open(fname,'w')
	f.write('ply\n')
	f.write('format ascii 1.0\n')
	f.write('element vertex ' + str(nV) + '\n')
	f.write('property float x\n')
	f.write('property float y\n')
	f.write('property float z\n')
	f.write('element face ' + str(nF) + '\n')
	f.write('property list uchar int vertex_indices\n')
	f.write('end_header\n')

	for i in range(0,nV):
		f.write('%0.4f %0.4f %0.4f\n' % (S[i,0],S[i,1],S[i,2]))  


	for i in range(0,nF):
    		f.write('3 %d %d %d\n' % (faces[i,0],faces[i,1],faces[i,2]))

	f.close()