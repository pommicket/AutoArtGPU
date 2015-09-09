__kernel void AutoFrame(__global float* output)
{
	unsigned int id = get_global_id(0);
	int width = <WIDTH>;

	int xInt = (id/3) % width;
	int yInt = (id/3) / width;
	float t = <FRAMENUMBER>;
	
	float x = (float)xInt;
	float y = (float)yInt;

	int channel = id % 3;
	
	if (channel == 0)
		output[id] = <RFUNCTION>;
	else if (channel == 1)
		output[id] = <GFUNCTION>;
	else
		output[id] = <BFUNCTION>;
}