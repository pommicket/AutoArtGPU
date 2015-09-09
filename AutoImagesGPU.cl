
__kernel void AutoImage(__global float *output)
{
	
	unsigned int id;
	int width;
	int xInt;
	int yInt;
	float x;
	float y;
	int channel;
	
	id = get_global_id(0);
	width = <WIDTH>;
	
	xInt = (id/3) % width;
	yInt = (id/3) / width;
	
	x = (float)xInt;
	y = (float)yInt;
	
	

	channel = id % 3;
	
	if (channel == 0)
		output[id] = <RFUNCTION>;
	else if (channel == 1)
		output[id] = <GFUNCTION>;
	else
		output[id] = <BFUNCTION>;
	
}
